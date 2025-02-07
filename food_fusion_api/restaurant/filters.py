from django_filters import rest_framework as filters
from .models import Restaurant

class RestaurantFilter(filters.FilterSet):
    keyword=filters.CharFilter(field_name='name',lookup_expr='icontains')
    type=filters.CharFilter(field_name='type',lookup_expr='icontains')
    class Meta:
        model=Restaurant
        fields=('type','name')