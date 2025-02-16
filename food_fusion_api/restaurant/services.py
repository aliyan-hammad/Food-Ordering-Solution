from .models import Restaurant,Branch
from food_fusion_api.services import haversine
from rest_framework.reverse import reverse
from .filters import RestaurantFilter
from address.models import Address
from rest_framework import serializers


def get_nearest_restaurant(request,user_lat,user_long):
    user_lat=float(user_lat)
    user_long=float(user_long)
    restaurants=Restaurant.objects.prefetch_related("branches__address")
    #for get a restaurant with it's all branches with there's address
    near_by=[]
    near_by=[
            {'name':restaurant.name,
            'cuisine':restaurant.type,
            'image': request.build_absolute_uri(restaurant.image.url) if restaurant.image and restaurant.image.url else None,
            'distance':f"{round(distance,2)}km",
            'branch_url': request.build_absolute_uri(
            reverse('branch-detail', 
            kwargs={'pk': branch.id})+f"?distance={round(distance,2)}Km")}
            for restaurant in restaurants
            for branch in restaurant.branches.all()
            if (distance:=haversine(user_lat,user_long,branch.address.latitude,branch.address.longitude))<=5.0
            ]
    return near_by
    
def get_all_restaurants(request):
    restaurant_filter=RestaurantFilter(request.query_params,queryset=Restaurant.objects.all())
    filtered_queryset=restaurant_filter.qs
    return filtered_queryset

def create_branch(user,validated_data):
    address_data=validated_data.pop('address',None)
    if not address_data:
        raise serializers.ValidationError({"error":"address is required"})
    restaurant=Restaurant.objects.get(owner=user)
    address=Address.objects.create(entity_type='branch',
                            entity_id=restaurant.id,
                            **address_data)
    branch=Branch.objects.create(address=address,restaurant=restaurant,**validated_data)
    if "contact" not in validated_data:
        branch.contact=restaurant.contact
        branch.save()
    return branch

def update_branch(instance,validated_data):
    address_data=validated_data.pop('address')
    if not address_data:
        raise serializers.ValidationError({"error":"address is required"})
    address_instance=instance.address
    for attr,value in address_data.items():
        setattr(address_instance,attr,value)
    address_instance.save()
    branch_id=instance.id
    if not branch_id:
        raise serializers.ValidationError({"error":"branch id is required"})
    branch=Branch.objects.get(id=branch_id)
    branch.contact=validated_data.get('contact',branch.contact)
    branch.open_time=validated_data.get('open_time',branch.open_time)
    branch.close_time=validated_data.get('close_time',branch.close_time)
    branch.save()
    return instance