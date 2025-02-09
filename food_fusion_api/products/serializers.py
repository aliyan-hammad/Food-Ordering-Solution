from rest_framework import serializers
from .models import Products
from restaurant.models import Restaurant


#for creating or retriev the products
class ProductCreateSerializer(serializers.ModelSerializer):
    restaurant_name=serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source='restaurant'
    )
    class Meta():
        model=Products
        fields=['restaurant_name','title','catagory','price','content','rating']

#for get a product detail
class ProductDetailSerializer(serializers.ModelSerializer):
    class Meta():
        model=Products
        fields=['title','price','rating','active']

        