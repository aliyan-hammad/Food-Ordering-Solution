from django.shortcuts import render , get_object_or_404
from .models import Address
from rest_framework import viewsets,status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny
from .serializers import UserAddressSerializer
# Create your views here.

class AddressViewSet(viewsets.ModelViewSet):
    queryset=Address.objects.all()
    serializer_class=UserAddressSerializer

@api_view(["PUT","GET"])
def address_get_or_put(request,id=None):
    if request.method == "GET":
        if id is not None:
            address=get_object_or_404(Address,id=id)
            serializer=UserAddressSerializer(address,many=False,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        addresses=Address.objects.filter(entity_type='user').all()
        serializer=UserAddressSerializer(addresses,many=True,context={'request':request})
        return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == 'PUT':
        address_instance=get_object_or_404(Address,id=id)
        if address_instance:
            serializer=UserAddressSerializer(address_instance,data=request.data,context={'request':request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

