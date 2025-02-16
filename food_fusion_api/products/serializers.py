from rest_framework import serializers
from .models import Products,Catagory

#for get a product detail
class ProductDetailSerializer(serializers.ModelSerializer):
    cuisine=serializers.ChoiceField(choices=Catagory.choices,source='catagory')
    url=serializers.HyperlinkedIdentityField(view_name='products-detail',lookup_field='pk')
    class Meta():
        model=Products
        fields=['url','image','cuisine','title','price','rating','content','active']

        