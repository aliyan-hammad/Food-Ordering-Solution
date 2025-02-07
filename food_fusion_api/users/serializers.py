from rest_framework import serializers
from .models import CustomUser


class UserRegistrationSerializer(serializers.HyperlinkedModelSerializer):
    password2=serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model=CustomUser
        fields=['phone_no','password','password2','first_name','last_name']
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
    

class UserLoginSerializer(serializers.Serializer):
    phone_no=serializers.CharField(required=True)
    password=serializers.CharField(required=True)


