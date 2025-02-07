from django.urls import path
from .views import ProductListCreateView,ProductDetailApiView,ProductUpdateDestroyView,ProductListView


urlpatterns=[
    path('product/create/',ProductListCreateView.as_view(),name='product-create'),
    path('product/list/',ProductListView.as_view(),name='product-list'),
    path('product/<int:pk>/',ProductDetailApiView.as_view(),name='products-detail'),
    path('product/<int:pk>/update/',ProductUpdateDestroyView.as_view(),name='product-update'),
    path('product/<int:pk>/delete/',ProductUpdateDestroyView.as_view(),name='product-destroy')

]