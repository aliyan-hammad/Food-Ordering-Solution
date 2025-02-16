from django.shortcuts import render,get_object_or_404
from rest_framework import viewsets,generics
from .models import Products
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductDetailSerializer
from .filters import ProductFilters
from restaurant.models import Restaurant
from .permissions import IsStaff
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

class ProductListView(generics.ListAPIView):
    queryset=Products.objects.all()
    serializer_class=ProductDetailSerializer
    filter_backends=[DjangoFilterBackend]
    filterset_class=ProductFilters
    lookup_field='pk'

class ProductDetailApiView(generics.RetrieveAPIView):
    queryset=Products.objects.all()
    serializer_class=ProductDetailSerializer
    lookup_field='pk'
    
class ProductsViewSet(viewsets.ModelViewSet):
    permission_classes=[IsStaff]
    serializer_class=ProductDetailSerializer
    parser_classes=(MultiPartParser,FormParser,JSONParser)
    filter_backends=[DjangoFilterBackend]
    filterset_class=ProductFilters
    lookup_field='pk'

    def get_queryset(self):
        return Products.objects.filter(restaurant__owner=self.request.user)
    
    def perform_create(self, serializer):
        user=self.request.user
        if serializer.is_valid(raise_exception=True):
            restaurant=Restaurant.objects.get(owner=user)
            title=serializer.validated_data.get('title')
            content=serializer.validated_data.get('content') or None
            if content is None:
                content=title
            serializer.save(restaurant=restaurant,content=content)
