from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers,generics
from administrator.models import *
from . models import *

from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from django.contrib.auth.password_validation import validate_password
from administrator.models import Address

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email

        return token

class RegisterSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(required=True,validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    phone_no=serializers.CharField(required=True,validators=[UniqueValidator(queryset=Consumer.objects.all())])
    class Meta:
        model = CustomUser
        fields = ('first_name','last_name','username','email','password','phone_no')


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields=("id","first_name","last_name","username","email","password","user_type")

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields='__all__'

class ConsumerSerializer(serializers.ModelSerializer):
    #add serializers.SerilizerMethodField() and define a function as below for getting associated values
    customuser=serializers.SerializerMethodField()
    address=AddressSerializer(many=True,read_only=True)
    class Meta:
        model=Consumer
        fields=["customuser","phone_no","address"]
    
    def get_customuser(self,obj):
        customuser=CustomUserSerializer(obj.consumer_admin).data
        return customuser

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['email','password']
