from django.urls import path,include
from .views import OrderView,CartViewSet,RestaurantOrderDetail
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('cart',CartViewSet,basename='cart-view')



urlpatterns=[
    path('',include(router.urls)),
    path('new/',OrderView.as_view(),name='order-create'),
    path('myorder/',OrderView.as_view(),name='order-list'),
    path('myorder/<str:id>/',OrderView.as_view(),name='order-detail'),
    path('record/',RestaurantOrderDetail.as_view(),name='order-record'),
]

