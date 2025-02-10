from django.shortcuts import render
from rest_framework import viewsets,generics,mixins,status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import Restaurant,Address,Branch
from .serializers import RestaurantDetailSerializer,RestaurantListSerializer,BranchCreateSerializer,NearestBranchSerializer,GetNearestBranchSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes,authentication_classes
from django.shortcuts import get_object_or_404
from .filters import RestaurantFilter
from rest_framework.permissions import IsAuthenticated,DjangoModelPermissions
from rest_framework.reverse import reverse
from food_fusion_api.services import haversine


@api_view(['GET','POST'])
def restaurant_retriev_view(request , pk=None):
    if request.method == 'GET':
        if pk is not None:
            restaurant=get_object_or_404(Restaurant,pk=pk)
            serializer=RestaurantDetailSerializer(restaurant,many=False,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
    if request.method == 'POST':
        serializer=RestaurantListSerializer(data=request.data,context={'request':request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# class RestaurantListCreateView(generics.ListCreateAPIView):
#     queryset=Restaurant.objects.all()
#     serializer_class=RestaurantListSerializer
    
class RestaurantDestroyUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Restaurant.objects.all()
    serializer_class=RestaurantListSerializer

class BranchCreateView(generics.CreateAPIView):
    permission_classes=[AllowAny]
    queryset=Branch.objects.all()
    serializer_class=BranchCreateSerializer
class BranchUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset=Branch.objects.all()
    serializer_class=BranchCreateSerializer

@api_view(['GET'])
def branch_retriev_view(request , pk=None,*args,**kwargs):
    if request.method == 'GET':
        if pk is not None:
            branch=get_object_or_404(Branch,pk=pk)
            distance=request.query_params.get('distance')
            serializer=NearestBranchSerializer(branch,many=False,context={'distance':distance})
    return Response(serializer.data,status=status.HTTP_200_OK)

class GetNearestRestaurants(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        try:
            user_lat=(request.GET.get('latitude'))
            user_long=(request.GET.get('longitude'))
            if user_lat or user_long:
                user_lat=float(user_lat)
                user_long=float(user_long)
                restaurants=Restaurant.objects.prefetch_related("branches__address")
                #for get a restaurant with it's all branches with there's address
                near_by=[]
                for restaurant in restaurants:
                    #for get a branche of each restaurant's branches
                    for branch in restaurant.branches.all():
                        branch_lat=branch.address.latitude
                        branch_long=branch.address.longitude
                        distance=haversine(user_lat,user_long,branch_lat,branch_long)
                        if distance <= 5.0:
                            near_by.append(
                                {'name':restaurant.name,
                                 'cusine':restaurant.type,
                                'distance':round(distance,2),
                                'branch_url': request.build_absolute_uri(
                                reverse('branch-detail', kwargs={'pk': branch.id})+f"?distance={round(distance,2)}",
                                )
                                }
                            )
                if near_by:
                    sorted_branch_list= sorted(near_by, key=lambda x: x["distance"])
                    total_restaurant=len(near_by)
                    return Response({'total_restaurant':total_restaurant,'nearest_restaurant':sorted_branch_list},status=200)

                else:
                    return Response({'message':'no nearest restaurant found'})
            else:
                restaurant_filter=RestaurantFilter(request.query_params,queryset=Restaurant.objects.all())
                filtered_queryset=restaurant_filter.qs
                serializer=RestaurantListSerializer(filtered_queryset,many=True,context={'request':request})
                return Response(serializer.data,status=status.HTTP_200_OK)
           
        except Exception as e:
            return Response({'error':str(e)},status=400)
        



