from django.db import models
from food_fusion_api.validators import validator_contact
from datetime import time,datetime
from address.models import Address
from django.contrib.auth import get_user_model

User=get_user_model()
# Create your models here.
class Type(models.TextChoices):
    barBQ='barBQ'
    fastfood='fastfood'
    barBQfastfood='barBQfastfood'


class Restaurant(models.Model):
    owner=models.ForeignKey(User,on_delete=models.SET_NULL,related_name='restaurant',null=True,blank=True)
    name=models.CharField(max_length=100,blank=False,null=False,unique=True)
    contact=models.CharField(max_length=11,blank=False,validators=[validator_contact])
    type=models.CharField(max_length=100,choices=Type.choices,default='None')
    image=models.ImageField(upload_to='restaurant/',null=True,blank=True)
    created_at=models.DateField(auto_now_add=True)
    updated_at=models.DateField(auto_now=True)

    @property
    def heigh_rated_products(self):
        return self.products.filter(rating__gte=4.0)
    def __str__(self):
            return f'{self.id} , {self.name}'


class Branch(models.Model):
    restaurant=models.ForeignKey(Restaurant,related_name='branches',on_delete=models.CASCADE)
    address=models.ForeignKey(Address,related_name='branch',on_delete=models.CASCADE)
    contact=models.CharField(max_length=11,blank=False,validators=[validator_contact],null=True)
    open_time=models.TimeField(default=time(9,0))
    close_time=models.TimeField(default=time(23,59))
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    @property
    def is_open(self):
        now=datetime.now().time()
        if self.open_time <= now <= self.close_time:
            return True
        return False
    
   
    def __str__(self):
        return f"{self.id},{self.address}"

    #when we get the instance of this model it will give us the output like this
    #self.id = branch.id , self.address = restaurant {self.entity_type , self.entity_id} , address=>{self.city} , {self.town} , {self.latitude,self.longitude}


