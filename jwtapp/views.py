from jwtapp.serializer import UserSerializer
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from . serializer  import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializers=UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)

class LoginView(APIView):
    def post(self,request):
        email=request.data['email']      
        password=request.data['password']  

        user=User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed("user is None")

        if not user.check_password(password):
            raise AuthenticationFailed("Incorrect Password")


        print(user)    

        payload={
            'id':user.id,
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
        }    
        print(payload)
        token=jwt.encode(payload,'secret',algorithm='HS256').decode('utf-8')
        print("dddddddddddd",token)

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data={
            "jwt":token
        }
        return response


class UserView(APIView):     
    def get(self,request):
        token=request.COOKIES.get('jwt')   
        print(token)
        if not token:
            return AuthenticationFailed("unauthenticated")
        try:
            pass
            payload=jwt.decode(token,'secret',algorithm=['HS256'])    
        except jwt.ExpiredSignatureError:
            return AuthenticationFailed("unauthenticated")

        print(payload)    

        user=User.objects.get(id=payload['id'])    
        print(user)
        serializer=UserSerializer(user)
        return Response(serializer.data)

        # return Response(token)


class LogoutView(APIView):
    def post(self,request):
        response = Response()
        response.delete_cookie('jwt')
        response.data={
            "logout":"logot successfully"
        }    
        return response    
        
         
      




