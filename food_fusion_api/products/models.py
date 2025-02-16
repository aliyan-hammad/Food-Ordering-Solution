from django.db import models
from decimal import Decimal
from restaurant.models import Restaurant
from django.core.exceptions import ValidationError
# Create your models here.
class Catagory(models.TextChoices):
    barBQ='barBQ'
    fastfood='fastfood'
    chiniesfood='chiniesfood'
    pakistanifood='pakistanifood'
    italianfood='italianfood'


class Products(models.Model):
    restaurant=models.ForeignKey(Restaurant,default=1,related_name="products",on_delete=models.CASCADE)
    image=models.ImageField(upload_to='products/',null=True,blank=True)
    title=models.CharField(max_length=100,blank=False,null=False,unique=True)
    catagory=models.CharField(max_length=50,choices=Catagory.choices,default='None')
    price=models.DecimalField(max_digits=10,decimal_places=2,default=Decimal('99.99'))
    content=models.TextField(null=True,blank=True)
    rating=models.DecimalField(max_digits=2,decimal_places=1,default=0.0,help_text='enter the rating between 0.0 and 5.0')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    active=models.BooleanField(default=True)
    def clean(self):
        if self.rating < 0.0 or self.rating > 5:
            raise ValidationError("rating should be between 0 - 5")
    def __str__(self) -> str:
        return f"{self.title} ,{self.image.url if self.image else "no image"} {self.rating}"
