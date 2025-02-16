from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import check_password
from .services import update_profile


class UserRegistrationSerializer(serializers.ModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=CustomUser
        fields=['phone_no','password','password2','first_name','last_name','email']
        extra_kwargs={
            'password':{'write_only':True}
            }
        
    def validate(self,attrs):
        password=attrs.get('password')
        password2=attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password confermation does not match")
        return attrs
    
    def create(self,validated_data):
        return CustomUser.objects.create_user(**validated_data)
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields=['first_name','last_name','email']
        
    def update(self,instance,validated_data):
        user=self.context['request'].user
        instance=update_profile(user,instance,validated_data)
        return instance

class PasswordChangeSerializer(serializers.Serializer):
    old_password=serializers.CharField(write_only=True,required=True)
    new_password=serializers.CharField(write_only=True,min_length=8,required=True)

    def validate_old_password(self,value):
        user=self.context['request'].user
        if not check_password(value,user.password):
            return serializers.ValidationError("old password is incorrect")
        return value
    
    def update(self,instance,validated_data):
        instance.set_password(validated_data['new_password'])
        instance.save()
        return instance

class UserLoginSerializer(serializers.Serializer):
    phone_no=serializers.CharField(required=True)
    password=serializers.CharField(required=True)

class CompleteProfileSerializer(serializers.ModelSerializer):
    class Meta():
        model=CustomUser
        fields=['id','first_name','last_name','phone_no','email','date_joined','last_login','is_active']

class VendorSerializer(serializers.ModelSerializer):
    restaurant=serializers.SerializerMethodField()
    class Meta():
        model=CustomUser
        fields=['id','first_name','phone_no','email','restaurant']
    
    def get_restaurant(self,obj):
        restaurant=obj.restaurant.first()
        return {"name":restaurant.name}