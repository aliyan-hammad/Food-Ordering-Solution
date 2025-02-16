from django.shortcuts import render , get_object_or_404
from .models import Address
from rest_framework import viewsets,status
from rest_framework.decorators import api_view
from .serializers import AddressSerializer
# Create your views here.

class AddressViewSet(viewsets.ModelViewSet):
    # queryset=Address.objects.all()
    serializer_class=AddressSerializer
    lookup_field="pk"
    def get_queryset(self):
        return Address.objects.filter(entity_type="user",entity_id=self.request.user.id)

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(entity_type='user',entity_id=user.id)