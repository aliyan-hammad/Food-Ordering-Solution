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
    path('<int:pk>/branch/',branch_retriev_view,name='branch-detail'),  #for get a branch
    path('<int:pk>/restaurant/',restaurant_retriev_view,name='restaurant-detail'), #for get a restaurant
    path('restaurant/list/',restaurant_retriev_view,name='restaurant-list'), # for get restaurant's list
    path('create/restaurant/',restaurant_retriev_view,name='create-instance'), #for create restaurnt
    path('<int:pk>/update/',RestaurantDestroyUpdateView.as_view(),name='update-instance'), #for updt rstrnt
    path('<int:pk>/delete/',RestaurantDestroyUpdateView.as_view(),name='destroye-instance'), #for dlt rstrnt
    path('branch/create/',BranchCreateView.as_view(),name='branch-list'), #for create a new branch
    path('<int:pk>/branch/update/',BranchUpdateDestroyView.as_view(),name='update-branch'), #for update branch
    path('<int:pk>/branch/delete/',BranchUpdateDestroyView.as_view(),name='update-delete'), #for delete branch
    path('nearbyrestaurant/',GetNearestRestaurants.as_view(),name='nearby-restaurants'), #to get nearest rstrnts
    path('nearbyrestaurant/<int:pk>/',GetNearestRestaurants.as_view(),name='nearby-restaurant') #to get specific rstrnt


]
