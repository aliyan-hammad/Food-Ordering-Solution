from django.db import models
from django.db.models import JSONField
from django.conf import settings
from restaurant.models import Branch,Restaurant,Address
from products.models import Products
import uuid


class Cart(models.Model):
    customer=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.customer}"
class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='ordercart',null=True)
    products=models.ForeignKey(Products,on_delete=models.CASCADE,related_name='ordercart')
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return f"{self.cart} , {self.products} , {self.quantity}"
class Checkout(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.SET_NULL,related_name='cart',null=True)
    cart_data=models.JSONField(null=True,blank=True)
    total_price=models.DecimalField(max_digits=10,decimal_places=2)
    address=models.ForeignKey(Address,on_delete=models.SET_NULL,null=True,related_name='items')
    order_status=models.CharField(max_length=100,default='Pending',null=False)
        
    def __str__(self):
        return f"{self.cart} , {self.address} , {self.order_status} , {self.total_price}"



class OrderItems(models.Model):
    id=models.UUIDField(default=uuid.uuid1,editable=False,unique=True,primary_key=True)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.SET_NULL,null=True)
    order_id=models.ForeignKey(Checkout,on_delete=models.CASCADE,related_name="order")
    created_at=models.DateTimeField(auto_now=True,null=True)
    updated_at=models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return (f" {self.id}   ,  {self.order_id}")