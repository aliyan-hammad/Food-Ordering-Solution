from django.contrib import admin
from django.urls import path,include
from .views import RestaurantViewSet,restaurant_retriev_view,BranchViewSet,branch_retriev_view,GetRestaurants
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register('owner',RestaurantViewSet,basename='restaurant-owner'),
router.register('restaurant-owner',BranchViewSet,basename='branch-owner')

urlpatterns = [
    path('',include(router.urls)),
    path('<int:pk>/branch/',branch_retriev_view,name='branch-detail'), 
    path('<int:pk>/restaurant/',restaurant_retriev_view,name='restaurant-detail'), 
    path('list/',GetRestaurants.as_view(),name='nearby-restaurants'), 


]
