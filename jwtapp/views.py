from jwtapp.serializer import UserSerializer
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from . serializer  import UserSerializer
from rest_framework.response import Response

# Create your views here.

class RegisterView(APIView):
    def post(self,request):
        serializers=UserSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        return Response(serializers.data)



