from rest_framework import viewsets,status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .serializers import OrderSerializer,CartCreateSerializer,OrderDetailSerializer,RestaurantOrderRecordSerializer
from .models import Order,Cart
from django.db import transaction
from .services import create_order_from_cart
from .permissions import IsAuthenticatedOrCustomer,IsStaff

#can get create update or delete the cart
class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartCreateSerializer
    lookup_field='pk'
    def get_queryset(self):
        return Cart.objects.filter(customer=self.request.user)


class OrderView(APIView):
    permission_classes=[IsAuthenticatedOrCustomer]
    def post(self,request):
        try:
            with transaction.atomic():
                user=request.user
                cart=Cart.objects.prefetch_related('ordercart').get(customer=user,ordered=False)
                order=create_order_from_cart(cart,user)
                serializer=OrderSerializer(order)
                response_data=serializer.data
                return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    def get(self,request,id=None):
        user=request.user
        if id is None:
            order=Order.objects.prefetch_related('order').filter(customer=user)
            if order is None:
                return Response({"message":"no any order to show you"})
            serializer=OrderDetailSerializer(order,many=True,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)
        
        else:
            order=get_object_or_404(Order.objects.prefetch_related('order'),id=id)
            if order.DoesNotExist:
                return Response({"message":"no order to show you"})
            serializer=OrderDetailSerializer(order,many=False,context={'request':request})
            return Response(serializer.data,status=status.HTTP_200_OK)

class RestaurantOrderDetail(APIView):
    permission_classes=[IsStaff]
    def get(self,request):
        user=self.request.user
        order=Order.objects.filter(restaurant__restaurant__owner=user).first()
        restaurant=order.restaurant.restaurant.name if order else None
        orders=Order.objects.filter(restaurant__restaurant__owner=user)
        serializer=RestaurantOrderRecordSerializer(orders,many=True,context={'request':request})
        return Response({"restaurant":restaurant,"record":serializer.data},status=status.HTTP_200_OK)


