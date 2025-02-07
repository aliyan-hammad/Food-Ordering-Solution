from django.urls import path,include
from .views import OrderView,CartViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('cart',CartViewSet,basename='cart-view')



urlpatterns=[
    path('',include(router.urls)),
    path('order/create/',OrderView.as_view(),name='order-create'),
    path('order/',OrderView.as_view(),name='order-view')
]

