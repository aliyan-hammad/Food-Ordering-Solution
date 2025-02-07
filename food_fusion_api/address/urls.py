from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import AddressViewSet,address_get_or_put


router=DefaultRouter()
router.register('address',AddressViewSet,basename='user-address')

urlpatterns=[
    path('user/',include(router.urls)),
    path('addresses/',address_get_or_put,name='address-list'),
    path('<int:id>/address/',address_get_or_put,name='address-detail'),
    path('<int:id>/address/update/',address_get_or_put,name='address-update')
]



