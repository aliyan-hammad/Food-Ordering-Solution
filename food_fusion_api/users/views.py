from django.shortcuts import render
from rest_framework.views import APIView,status
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer,UserLoginSerializer,PasswordChangeSerializer,CompleteProfileSerializer,UserProfileSerializer,VendorSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .services import get_user
from .permissions import IsAuthenticatedOrAllowAny,IsAdminUser
from.models import CustomUser
from rest_framework.permissions import IsAuthenticated

# Create your views here.
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class GetCreateUpdateProfile(APIView):
    permission_classes=[IsAuthenticatedOrAllowAny]
    def post(self,request,format=None):
        serializer=UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({"message":"user registered succesful"},status=status.HTTP_201_CREATED)
        return Response({"message":"user registered failed"},status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request):
        user=request.user
        serializer=UserProfileSerializer(user,data=request.data,partial=True,context={'request':request})
        
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'message':f'thanks! {user.first_name} profile completed successfully'},status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        user=self.request.user
        customer=CustomUser.objects.get(id=user.id)
        serializer=CompleteProfileSerializer(customer,many=False,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class ChangePassword(APIView):
    permission_classes=[IsAuthenticatedOrAllowAny]
    def put(self,request,format=None):
        serializer=PasswordChangeSerializer(data=request.data,context={'request':request})
        if serializer.is_valid():

            serializer.update(request.user,serializer.validated_data)
            return Response({'message':'password changed succesfully'},status=status.HTTP_200_OK)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    permission_classes=[IsAuthenticatedOrAllowAny]
    def post(self,request,format=None):
        serializer=UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):

            data=serializer.data
            user=get_user(data)
            if user is None:
                return Response({'error':'invalid user or password'},status=status.HTTP_400_BAD_REQUEST)
            
            token=get_tokens_for_user(user)
            if not user.first_name or not user.email:
                return Response({'message':'user login successful',
                                'note':'please complete your profile so we may know you','user_id':user.id,
                                'token':token},status=status.HTTP_200_OK)
            
            return Response({'message':'user login successful',
                            "message":f"welcome {user.first_name}",
                            'user_id':user.id,
                            'token':token},status=status.HTTP_200_OK)
        
@api_view(["POST"])
def logout(request):
    try:
        refresh_token=request.data.get('refresh')
        if  not refresh_token:
            return Response({'error':'refresh token is required'},status=status.HTTP_400_BAD_REQUEST)
        
        token=RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message':'logout successfully'},status=status.HTTP_200_OK)
    
    except Exception as e:
        return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)



 
class GetCustomersRecord(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        customers=CustomUser.objects.filter(is_active=True)
        serializer=CompleteProfileSerializer(customers,many=True,context={"request":request})
        total_customers=len(customers)
        return Response({"total customers":total_customers,"Profile":serializer.data},status=status.HTTP_200_OK)
    
class GetVendorDetail(APIView):
    permission_classes=[IsAdminUser]
    def get(self,request):
        staff=CustomUser.objects.filter(is_staff=True).prefetch_related('restaurant')
        serializer=VendorSerializer(staff,many=True)
        total_vendors=len(staff)
        return Response({"total vendors":total_vendors,"Profile":serializer.data},status=status.HTTP_200_OK)
    
