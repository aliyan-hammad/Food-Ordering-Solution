from rest_framework import serializers
from .models import *
from django.db import transaction
from address.models import Address
from address.serializers import AddressSerializer
# from food_fusion_api.services import haversine

class CartItemsSerializer(serializers.ModelSerializer):
    restaurant=serializers.CharField(source='products.restaurant.name',read_only=True)
    branch=serializers.PrimaryKeyRelatedField(queryset=Branch.objects.all())
    total_price=serializers.SerializerMethodField(read_only=True)
    class Meta():
        model=CartItem
        fields=['restaurant','products','quantity','branch','total_price']
    def get_total_price(self,obj):
        return float(obj.products.price*obj.quantity)
class CartCreateSerializer(serializers.ModelSerializer):
    ordercart=CartItemsSerializer(many=True)
    class Meta():
        model=Cart
        fields=['ordercart']

    def validate(self,validated_data):
        ordercart=validated_data.get('ordercart',[])
        if ordercart:
            for orderitem in ordercart:
                products=orderitem['products']
                branch=orderitem['branch']
                if products.restaurant != branch.restaurant:
                    raise serializers.ValidationError({'error':f"{products.title} is not from the selected branch{branch.address}"})
        return validated_data
    def create(self,validated_data):
        try:
            with transaction.atomic():
                ordercart=validated_data.pop('ordercart')
                user=self.context['request'].user
                cart,create=Cart.objects.get_or_create(customer=user,ordered=False)
                cartitems={cartitem.products.id:cartitem for cartitem in CartItem.objects.filter(cart=cart)}
                for item in ordercart:
                    product_id=item['products'].id
                    if product_id in cartitems:
                        existing_cartitem=cartitems[product_id]
                        existing_cartitem.quantity+=item.get('quantity',1)
                        existing_cartitem.branch=item['branch']
                        existing_cartitem.save() 
                    else:
                        CartItem.objects.create(cart=cart,**item)  
            return cart
        except Exception as e:
            raise serializers.ValidationError({'error':str(e)})

    def update(self,instance,validated_data):
        with transaction.atomic():
            user=self.context['request'].user
            if user == instance.customer:
                item_validated_data=validated_data.get("ordercart") #python dictionary type
                if item_validated_data:
                    cartitem_prod_ids=[]
                    for item in item_validated_data:
                        cartitem_prod_ids.append(item['products'].id)
                    cartitems=CartItem.objects.filter(cart=item['cart'].id)
                    for cartitem_instance in cartitems:
                        if cartitem_instance.products.id not in cartitem_prod_ids:
                            CartItem.objects.get(cart=item['cart'].id,products=cartitem_instance.products).delete()
                    for item in item_validated_data:
                        try:
                            cart_id=item['cart'].id
                            product_id=item['products'].id
                            quantity=item.get('quantity',1)
                            if quantity <=0:
                                raise serializers.ValidationError({'error':'quantity should be atleast 1'})
                            cartitem=CartItem.objects.get(cart=cart_id,products=product_id)
                            if cartitem:
                                cartitem.quantity=quantity
                                cartitem.save()
                        except:
                            CartItem.objects.create(
                                cart=item['cart'],
                                products=item['products'],
                                quantity=item.get('quantity',1))
                else:
                    raise serializers.ValidationError({'error':'cart is empty'})
            else:
                raise serializers.ValidationError({'error':'user is not allowed to this cart'})
        return instance

class CheckoutSerializer(serializers.ModelSerializer):
    distance=serializers.SerializerMethodField(read_only=True)
    address=AddressSerializer()
    cart=CartCreateSerializer()
    class Meta():
        model=Checkout
        fields=['address','cart','total_price','order_status','distance']
    def get_distance(self,obj):
        return obj.distance
class OrderItemSerializer(serializers.ModelSerializer):
    order_id=CheckoutSerializer()
    phone_no=serializers.CharField(source='user.phone_no',read_only=True)

    class Meta():
        model=OrderItems
        fields=['id','phone_no','order_id']


class OrderDetailSerializer(serializers.ModelSerializer):
    total_price=serializers.IntegerField(source='order_id.total_price',read_only=True)
    order_status=serializers.CharField(source='order_id.order_status',read_only=True)
    cart=CartCreateSerializer(source='order_id.cart')
    class Meta():
        model=OrderItems
        fields=['id','cart','total_price','order_status']

    
            
  
