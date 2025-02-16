from django.shortcuts import render
from rest_framework import generics,status,viewsets
from rest_framework.views import APIView
from .models import Restaurant,Branch
from .serializers import RestaurantDetailSerializer,RestaurantListSerializer,BranchCreateSerializer,NearestBranchSerializer,BranchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
from .services import get_nearest_restaurant,get_all_restaurants
from .permissions import IsAuthenticatedOrRestaurantOwner,IsStaff
from rest_framework.parsers import MultiPartParser,FormParser,JSONParser

@api_view(['GET'])
def restaurant_retriev_view(request , pk=None):
    if request.method == 'GET':
        if pk is not None:
            restaurant=get_object_or_404(Restaurant,pk=pk)
            serializer=RestaurantListSerializer(restaurant,many=False,context={'request':request})

            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
class RestaurantViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticatedOrRestaurantOwner]
    serializer_class=RestaurantDetailSerializer
    parser_classes=(MultiPartParser,FormParser,JSONParser)
    lookup_field='pk'
    def get_queryset(self):
        return Restaurant.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        if serializer.is_valid(raise_exception=True):
            user=self.request.user
            serializer.save(owner=user)
            user.is_staff=True
            user.save()

    def perform_destroy(self, instance):
        user=self.request.user
        instance.delete()
        user.is_staff=False
        user.save()

class BranchViewSet(viewsets.ModelViewSet):
    permission_classes=[IsStaff]
    serializer_class=BranchCreateSerializer
    lookup_field='pk'
    def get_queryset(self):
        return Branch.objects.filter(restaurant__owner=self.request.user)

@api_view(['GET'])
def branch_retriev_view(request , pk=None,*args,**kwargs):
    if request.method == 'GET':
        if pk is not None:
            branch=get_object_or_404(Branch,pk=pk)

            distance=request.query_params.get('distance')
            if distance:
                serializer=NearestBranchSerializer(branch,many=False,context={'distance':distance,'request':request})

            else:   
                serializer=BranchSerializer(branch,many=False,context={'request':request})
    return Response(serializer.data,status=status.HTTP_200_OK)

class GetRestaurants(APIView):
    def get(self,request):
        try:
            user_lat=(request.GET.get('latitude'))
            user_long=(request.GET.get('longitude'))

            if user_lat or user_long:
                near_by=get_nearest_restaurant(request,user_lat,user_long)
                if not near_by:
                    return Response({"message":"no nearest restaurant food to this location"})
                
                sorted_branch_list= sorted(near_by, key=lambda x: x["distance"])
                total_restaurant=len(near_by)

                return Response({'total_restaurant':total_restaurant,'nearest_restaurant':sorted_branch_list},status=status.HTTP_200_OK)
            
            restaurants=get_all_restaurants(request)

            serializer=RestaurantListSerializer(restaurants,many=True,context={'request':request})

            return Response({"message":'please make sure your location for order',"Restaurants":serializer.data},status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response({'error':str(e)},status=400)
        



