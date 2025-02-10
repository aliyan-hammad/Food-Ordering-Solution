from rest_framework import serializers,status,exceptions
from .models import Restaurant , Branch
from products.serializers import ProductDetailSerializer
from rest_framework.request import Request
from django.db import transaction
from address.models import Address
from address.serializers import AddressSerializer
import logging
logger=logging.getLogger(__name__)

#serialize the data to show the nearest restaurants.......
class GetNearestBranchSerializer(serializers.HyperlinkedModelSerializer):
    restaurant_name=serializers.CharField(source='restaurant.name',read_only=True)
    distance=serializers.FloatField(read_only=True)
    class Meta():
        model=Branch
        fields=['url','restaurant_name','distance']

#serializer for creating branch
class BranchCreateSerializer(serializers.HyperlinkedModelSerializer):
    address=AddressSerializer()
    restaurant_id=serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(),
        source='restaurant'
    )
    class Meta():
        model=Branch
        fields=['restaurant_id','contact','open_time','close_time','address']

    def create(self,validated_data):
            try:
                with transaction.atomic():
                    address_data=validated_data.pop('address',None)
                    if address_data:
                        restaurant=validated_data.get('restaurant')
                        if restaurant:
                            address=Address.objects.create(entity_type='branch',
                                                    entity_id=restaurant.id,
                                                    **address_data)
                            branch=Branch.objects.create(address=address,**validated_data)
                        else:
                            raise serializers.ValidationError({'restaurant':'restaurant is required'})
                    else:
                        raise serializers.ValidationError({'address':"address fields cannot be empty"})
                return branch
            except Exception as e:
                raise serializers.ValidationError({'error':f"{e}"})
    def update(self,instance,validated_data):
        try:
            with transaction.atomic():
                address_data=validated_data.pop('address')
                if address_data:
                    address_instance=instance.address
                    for attr,value in address_data.items():
                        setattr(address_instance,attr,value)
                    address_instance.save()
                    branch_id=instance.id
                    if branch_id:
                        branch=Branch.objects.get(id=branch_id)
                        branch.contact=validated_data.get('contact',branch.contact)
                        branch.open_time=validated_data.get('open_time',branch.open_time)
                        branch.close_time=validated_data.get('close_time',branch.close_time)
                        branch.save()
                    else:
                        raise serializers.ValidationError('branch does not exist')
                else:
                    raise serializers.ValidationError({'address':'address must be required'})
        except Exception as e:
            raise serializers.ValidationError({'error':f'{e}'})
        return instance

#use for get nearest branch
class NearestBranchSerializer(serializers.ModelSerializer):
    address=AddressSerializer(many=False,read_only=True)
    restaurant_name=serializers.CharField(source='restaurant.name',read_only=True)
    distance=serializers.SerializerMethodField(read_only=True)
    products=serializers.SerializerMethodField()
    class Meta():
        model=Branch
        fields=['restaurant_name','address','contact','is_open','distance','products']
    def get_distance(self,obj):
        return self.context.get('distance')
    def get_products(self,obj):
        products=obj.restaurant.products.all()
        return ProductDetailSerializer(products,many=True).data

class BranchSerializer(serializers.ModelSerializer):
    address=AddressSerializer(many=False)
    branch_no=serializers.SerializerMethodField(read_only=True)
    class Meta():
        model=Branch
        fields=['branch_no','contact','address','is_open']
    def get_branch_no(self,obj):
        restaurant=obj.restaurant
        branches=restaurant.branches.order_by('id')
        branch_no=list(branches).index(obj)+1
        return branch_no
#serializer for retriev restaurants
class RestaurantListSerializer(serializers.HyperlinkedModelSerializer):
    heigh_rated_products=ProductDetailSerializer(many=True,required=False)
    cusine=serializers.CharField(source='type')
    class Meta():
        model=Restaurant
        fields=['url','id','name','contact','cusine','heigh_rated_products']
         
#serializer for get a specific restaurant to see it's branches
class RestaurantDetailSerializer(serializers.HyperlinkedModelSerializer):
    branches=BranchSerializer(many=True,read_only =True)
    class Meta():
        model=Restaurant
        fields=['name','type','branches']