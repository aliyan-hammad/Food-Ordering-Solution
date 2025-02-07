from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view


# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class UserRegistrationView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user=serializer.save()
            return Response({"message":"user registered succesful"},status=status.HTTP_201_CREATED)
        return Response({"message":"user registered failed"},status=status.HTTP_400_BAD_REQUEST)
class UserLoginView(APIView):
    permission_classes=[AllowAny]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            phone_no=serializer.data.get("phone_no")
            password=serializer.data.get("password")
            user=authenticate(phone_no=phone_no,password=password)
            if user is not None:
                token=get_tokens_for_user(user)
                return Response({'message':'user login successful',
                                 'token':token},status=status.HTTP_200_OK)
            else:
                return Response({'error':'invalid user or password'},status=status.HTTP_400_BAD_REQUEST)
        
@api_view(["POST"])
def logout(request):
    try:
        if request.method == "POST":
            refresh_token=request.data.get('refresh')
            if  not refresh_token:
                return Response({'error':'refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
            token=RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message':'logout successfully'},status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)