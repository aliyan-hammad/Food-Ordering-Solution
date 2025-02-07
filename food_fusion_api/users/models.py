from django.db import models
from django.contrib.auth.models import AbstractUser,PermissionsMixin,BaseUserManager,User
from food_fusion_api.validators import validator_contact
from restaurant.models import Address
# Create your models here.

class AccountManager(BaseUserManager):
    def create_user(self,phone_no,password=None,password2=None,**extra_fields):
        if not phone_no:
            raise ValueError('phone_no field must be set')
        # email=self.normalize_email(email)
        user=self.model(phone_no=phone_no,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,phone_no,password=None,**extra_fields):
        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_superuser",True)
        return self.create_user(phone_no,password,**extra_fields)
    
class CustomUser(AbstractUser,PermissionsMixin):
    username=None
    phone_no=models.CharField(max_length=11,validators=[validator_contact],blank=False,unique=True)
    USERNAME_FIELD='phone_no'
    # EMAIL_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=AccountManager()
    def __str__(self):
        return self.first_name+""+self.phone_no