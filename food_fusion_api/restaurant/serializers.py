from rest_framework import serializers
from .models import Restaurant , Branch , Type
from products.serializers import ProductDetailSerializer
from django.db import transaction
import logging
logger=logging.getLogger(__name__)
from .services import create_branch,update_branch


#serializer for creating branch
class BranchCreateSerializer(serializers.HyperlinkedModelSerializer):
    address=serializers.CharField(read_only=True)
    restaurant=serializers.CharField(source='restaurant.name',read_only=True)
    class Meta():
        model=Branch
        fields=['restaurant','id','contact','open_time','close_time','address']

    def create(self,validated_data):
            try:
                with transaction.atomic():
                    user=self.context['request'].user
                    branch=create_branch(user,validated_data)
                    return branch
            except Exception as e:
                raise serializers.ValidationError({'error':f"{e}"})
            
    def update(self,instance,validated_data):
        try:
            with transaction.atomic():
                instance=update_branch(instance,validated_data)
                return instance
        except Exception as e:
            raise serializers.ValidationError({'error':f'{e}'})

#use for get nearest branch
class NearestBranchSerializer(serializers.ModelSerializer):
    address=serializers.CharField(read_only=True)
    restaurant_name=serializers.CharField(source='restaurant.name',read_only=True)
    distance=serializers.SerializerMethodField(read_only=True)
    products=serializers.SerializerMethodField()
    image=serializers.ImageField(source='restaurant.image',read_only=True)

    class Meta():
        model=Branch
        fields=['restaurant_name','image','address','contact','is_open','distance','products']

    def get_distance(self,obj):
        return self.context.get('distance')
    
    def get_products(self,obj):
        products=obj.restaurant.products.all()
        return ProductDetailSerializer(products,many=True,context=self.context).data
     

class BranchSerializer(serializers.ModelSerializer):
    address=serializers.CharField(read_only=True)
    branch_no=serializers.SerializerMethodField(read_only=True)
    class Meta():
        model=Branch
        fields=['id','branch_no','contact','address','open_time','close_time']
    def get_branch_no(self,obj):
        restaurant=obj.restaurant
        branches=restaurant.branches.order_by('id')
        branch_no=list(branches).index(obj)+1
        return branch_no
    
#serializer for retriev restaurants
class RestaurantListSerializer(serializers.HyperlinkedModelSerializer):
    heigh_rated_products=ProductDetailSerializer(many=True,required=False,read_only=True)
    cusine=serializers.CharField(source='type')
    class Meta():
        model=Restaurant
        fields=['url','id','image','name','contact','cusine','heigh_rated_products']

#serializer for get a specific restaurant to see it's branches
class RestaurantDetailSerializer(serializers.HyperlinkedModelSerializer):
    branches=BranchSerializer(many=True,read_only =True)
    cuisine=serializers.ChoiceField(choices=Type.choices,source='type')
    class Meta():
        model=Restaurant
        fields=['id','image','name','cuisine','contact','branches']