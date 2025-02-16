from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import ProductDetailApiView,ProductsViewSet,ProductListView

router=DefaultRouter()
router.register('owner',ProductsViewSet,basename='restaurant-owner')

urlpatterns=[
    path('',include(router.urls)),
    path('list',ProductListView.as_view(),name='product-list'),
    path('<int:pk>/',ProductDetailApiView.as_view(),name='products-detail'),
]