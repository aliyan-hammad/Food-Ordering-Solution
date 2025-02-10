from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
# from .models import Restaurant
from .views import RestaurantDestroyUpdateView,restaurant_retriev_view,BranchCreateView,BranchUpdateDestroyView,branch_retriev_view,GetNearestRestaurants
# from products.views import ProductViewSet,ProductDetailApiView
# from orders.views import OrderCartViewSet

# router=routers.DefaultRouter()
# router.register(f'products',ProductViewSet)
# router.register(f'orders',OrderCartViewSet)
urlpatterns = [
    path('<int:pk>/branch/',branch_retriev_view,name='branch-detail'), 
    path('<int:pk>/restaurant/',restaurant_retriev_view,name='restaurant-detail'), 
    # path('restaurant/list/',restaurant_retriev_view,name='restaurant-list'), 
    path('restaurant/',restaurant_retriev_view,name='create-restaurant'),
    path('<int:pk>restaurant/',RestaurantDestroyUpdateView.as_view(),name='destroye-update-restaurant'),
    path('branch/',BranchCreateView.as_view(),name='branch-create'), 
    path('<int:pk>branch/',BranchUpdateDestroyView.as_view(),name='destroye-update-branch'),
    path('restaurants/',GetNearestRestaurants.as_view(),name='nearby-restaurants'), 
    # path('<int:pk>/restaurant/',GetNearestRestaurants.as_view(),name='nearby-restaurant') 


]
