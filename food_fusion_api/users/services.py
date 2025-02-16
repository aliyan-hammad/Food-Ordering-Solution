from .models import CustomUser
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers


def get_user(data):
    phone_no=data.get("phone_no")
    password=data.get("password")
    user=authenticate(phone_no=phone_no,password=password)
    return user
       
        
def update_profile(user,instance,validated_data):
    if user.id != instance.id:
        raise serializers.ValidationError("you are not allowed to edit this profile")
    for attr,value in validated_data.items():
        setattr(instance,attr,value)
    instance.save()
    return instance

