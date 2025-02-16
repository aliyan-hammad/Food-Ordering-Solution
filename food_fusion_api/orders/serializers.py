from rest_framework import serializers
from .models import *
from django.db import transaction
from .services import create_cart_with_items,update_cart
# from food_fusion_api.services import haversine

class CartItemsSerializer(serializers.ModelSerializer):
    branch=serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    total_price=serializers.SerializerMethodField(read_only=True)
    class Meta():
        model=CartItem
        fields=['product','quantity','branch','total_price']

    def get_total_price(self,obj):
        return float(obj.product.price*obj.quantity)


class CartCreateSerializer(serializers.ModelSerializer):
    items=CartItemsSerializer(many=True,source='ordercart')
    restaurant=serializers.SerializerMethodField()
    class Meta():
        model=Cart
        fields=['restaurant','id','items','ordered']
        
    def get_restaurant(self,obj):
        cartitem=obj.ordercart.first()
        if cartitem:
            return cartitem.product.restaurant.name
        return None

    def validate(self,validated_data):
        ordercart=validated_data.get('ordercart',[])
        if ordercart:
            for orderitem in ordercart:
                product=orderitem['product']
                branch=orderitem['branch']
                if product.restaurant != branch.restaurant:
                    raise serializers.ValidationError({'error':f"{product.title} is not from the selected restaurant"})
        return validated_data

    def create(self,validated_data):
        try:
            with transaction.atomic():
                user=self.context['request'].user
                cart=create_cart_with_items(user,validated_data)
            return cart
        except Exception as e:
            raise serializers.ValidationError({'error':str(e)})

    def update(self,instance,validated_data):
        with transaction.atomic():
            user=self.context['request'].user
            instance=update_cart(user,instance,validated_data)
        return instance

class OrderItemSerializer(serializers.ModelSerializer):
    product_name=serializers.CharField(source='product.title')
    price=serializers.CharField(source='product.price')
    class Meta():
        model=OrderItems
        fields=['product_name','price','quantity']

class OrderSerializer(serializers.ModelSerializer):
    distance=serializers.SerializerMethodField(read_only=True)
    ordered_items=serializers.SerializerMethodField(read_only=True)
    address=serializers.CharField(source='delievery_address',read_only=True)
    class Meta():
        model=Order
        fields=['id','address','ordered_items','total_price','order_status','distance']
    def get_distance(self,obj):
        return obj.distance
    def get_ordered_items(self,obj):
        ordered_items=obj.order.all()
        return OrderItemSerializer(ordered_items,many=True).data



class OrderDetailSerializer(serializers.ModelSerializer):
    order_items=serializers.SerializerMethodField(read_only=True)
    class Meta():
        model=Order
        fields=['id','order_items','total_price','order_status']

    def get_order_items(self,obj):
        order_items=obj.order.all()
        return OrderItemSerializer(order_items,many=True).data
        
  
class RestaurantOrderRecordSerializer(serializers.ModelSerializer):
    name=serializers.CharField(source='customer.first_name',read_only=True)
    branch=serializers.CharField(source='restaurant',read_only=True)
    delievered_at=serializers.CharField(source='delievery_address',read_only=True)
    class Meta():
        model=Order
        fields=["id","customer","name","branch","delievered_at","total_price","order_status"]