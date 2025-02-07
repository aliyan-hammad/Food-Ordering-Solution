from django.db import models

# Create your models here.
class Town(models.TextChoices):
    Fazaltown='Fazaltown'
    Faisaltown='Faisaltown'
    Shahkhalid='Shahkhalid'
    GulzareQaid='GulzareQaid'
    AirportSociety='AirportSociety'
    Gulraiz='Gulraiz'
    Goritown='Goritown'
    Koraltown='Koraltown'
class City(models.TextChoices):
    Karachi='Karachi'
    Islamabad='Islamabad'
    Rawalpindi='Rawalpindi'
    Lahore='Lahore'
    Hyderabad='Hyderabad'
    Multan='Multan'
class Address(models.Model):
    address_lane1=models.CharField(max_length=100,null=False)
    address_lane2=models.CharField(max_length=100,null=True,help_text='Optional')
    entity_type=models.CharField(max_length=50)
    entity_id=models.IntegerField()
    country=models.CharField(max_length=100,null=False,default='Pakistan')
    postal_code=models.CharField(max_length=10,default='4646')
    city=models.CharField(max_length=100,choices=City.choices,blank=False)
    town=models.CharField(max_length=50,choices=Town.choices,blank=False)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.id} , {self.address_lane1} , {self.country} , {self.city} , {self.town}"