from django.shortcuts import render
from rest_framework import viewsets,generics
from .models import Products
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductCreateSerializer,ProductDetailSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly,IsAdminUser
from .filters import ProductFilters
# Create your views here.
class ProductListCreateView(generics.ListCreateAPIView):
    permission_classes=[IsAdminUser]
    queryset=Products.objects.all()
    serializer_class=ProductCreateSerializer
class ProductListView(generics.ListAPIView):
    # permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=Products.objects.all()
    serializer_class=ProductDetailSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=ProductFilters
class ProductDetailApiView(generics.RetrieveAPIView):
    # permission_classes=[IsAuthenticatedOrReadOnly]
    queryset=Products.objects.all()
    serializer_class=ProductDetailSerializer
    
class ProductUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=[IsAdminUser]
    queryset=Products.objects.all()
    serializer_class=ProductCreateSerializer