from rest_framework import generics,viewsets,mixins,status
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import CheckoutSerializer,CartCreateSerializer,OrderItemSerializer,OrderDetailSerializer
from .models import Checkout,Cart,CartItem,OrderItems
from rest_framework.permissions import AllowAny
from address.models import Address
from django.db import transaction


#can get create update or delete the cart
class CartViewSet(viewsets.ModelViewSet):
    queryset=Cart.objects.all()
    serializer_class=CartCreateSerializer


class OrderView(APIView):
    def post(self,request):
        try:
            with transaction.atomic():
                user=request.user
                cart=Cart.objects.prefetch_related('ordercart').get(customer=user)
                try:
                    address=Address.objects.get(entity_type='user',entity_id=user.id)
                except:
                    return Response({'error':'we are missing your address'})
                total_price=sum(cartitem.products.price*cartitem.quantity for cartitem in cart.ordercart.all())
                cart_data=CartCreateSerializer(cart).data
                checkout=Checkout.objects.create(
                    cart=cart,
                    address=address,
                    total_price=total_price,
                    cart_data=cart_data,
                    order_status='confermed'
                )
                orderitem=OrderItems.objects.create(order_id=checkout,user=user)
                serializer=OrderItemSerializer(orderitem)
                cart.delete()
                response_data=serializer.data
                return Response(response_data,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    def get(self,request,pk=None):
        if pk is None:
            user=request.user
            orderlist=OrderItems.objects.filter(user=user).all()
            if orderlist:
                serializer=OrderDetailSerializer(orderlist,many=True,context={'request':request})
                return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)



