from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CustomUserAdmin(UserAdmin):
    model=CustomUser
    list_display=['phone_no','is_staff','is_superuser','first_name','last_login']
    list_filter=['is_staff','is_superuser']
    search_fields=['phone_no','first_name']
    ordering=['phone_no']
    fieldsets=(
        (None, {'fields':('phone_no','password')}),
        ('Personal info',{'fields':('first_name','last_name')}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important dates',{'fields':('last_login','date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("phone_no","usable_password","password1","password2"),
            },
        ),
    )

admin.site.register(CustomUser,CustomUserAdmin)