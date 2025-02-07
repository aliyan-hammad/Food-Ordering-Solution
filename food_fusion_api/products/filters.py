from django_filters import rest_framework as filters
import django_filters
from .models import Products

class ProductFilters(django_filters.FilterSet):
    max_price=django_filters.NumberFilter(field_name='price',lookup_expr='lte')
    min_price=django_filters.NumberFilter(field_name='price',lookup_expr='gte')
    title=django_filters.CharFilter(field_name='title',lookup_expr='icontains')
    catagory=django_filters.CharFilter(field_name='catagory',lookup_expr='icontains')
    class Meta():
        model=Products
        fields=('catagory','title','max_price','min_price')