from django.db import models
from django.db.models import JSONField
from django.contrib.auth import get_user_model
from address.models import Address
from products.models import Products
import uuid
from restaurant.models import Branch
from food_fusion_api.services import haversine

User=get_user_model()

class Cart(models.Model):
    customer=models.ForeignKey(User,on_delete=models.CASCADE)
    ordered=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.customer}"
class CartItem(models.Model):
    branch=models.ForeignKey(Branch,on_delete=models.CASCADE,related_name='ordercart',null=True)
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='ordercart',null=True)
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='ordercart')
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.cart} , {self.product} , {self.quantity}"
class Order(models.Model):
    id=models.UUIDField(default=uuid.uuid1,editable=False,unique=True,primary_key=True)
    customer=models.ForeignKey(User,on_delete=models.SET_NULL,null=True)
    restaurant=models.ForeignKey(Branch,on_delete=models.SET_NULL,null=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    delievery_address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,related_name='items')
    order_status=models.CharField(max_length=100,default='Pending',null=False)
    created_at=models.DateTimeField(auto_now=True,null=True)
    delevered_at=models.DateTimeField(null=True,blank=True)

    @property
    def distance(self):
        if not self.delievery_address:
            return None
        latitude=self.delievery_address.latitude
        longitude=self.delievery_address.longitude
        if latitude is None or longitude is None:
            return None
        branch=self.restaurant
        branch_lat=branch.address.latitude
        branch_long=branch.address.longitude
        if branch_lat is None or branch_long is None:
            return None
        distance=haversine(lat1=latitude,lon1=longitude,lat2=branch_lat,lon2=branch_long)
        distance=round(distance,2)
        return distance
    def __str__(self):
        return f" {self.delievery_address} , {self.order_status} , {self.total_price}"

class OrderItems(models.Model):
    order_id=models.ForeignKey(Order,on_delete=models.CASCADE,related_name="order")
    product=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='order_items',null=True)
    quantity=models.PositiveIntegerField(default=1)
    created_at=models.DateTimeField(auto_now=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return (f" {self.order_id} , {self.product} , {self.quantity}")