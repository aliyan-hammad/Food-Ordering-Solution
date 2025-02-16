from .models import OrderItems,CartItem,Cart,Order
from address.models import Address
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

def calculate_total(cart):
    total_price=sum(cartitem.product.price*cartitem.quantity for cartitem in cart.ordercart.all())
    return total_price
def get_address(user):
    try:
        address=Address.objects.get(entity_type='user',entity_id=user.id)
        return address
    except:
        return None

    

def create_order_from_cart(cart,user):
    if not cart:
        raise ValueError('cart does not exist')
    address=get_address(user)
    if not address:
        raise ValueError("sorry! we are missing your address")
    cartitems=cart.ordercart.all()
    branch=cartitems.first().branch
    order=Order.objects.create(
        customer=user,
        total_price=calculate_total(cart),
        delievery_address=address,
        order_status="confirmed",
        restaurant=branch
    )
    orderitems=[
        OrderItems(order_id=order,product=item.product,quantity=item.quantity) for item in cartitems
    ]
    OrderItems.objects.bulk_create(orderitems)
    
    cart.delete()
    return order

def create_cart_with_items(user,validated_data):
        ordercart=validated_data.pop('ordercart')
        if not ordercart:
            raise ValidationError('ordercart is empty!!!')
        
        cart,create=Cart.objects.get_or_create(customer=user,ordered=False)
        cartitems={cartitem.product.id:cartitem for cartitem in CartItem.objects.filter(cart=cart)}
        new_branch=ordercart[0]['branch']

        if cartitems:
            existing_branch=next(iter(cartitems.values())).branch
            if new_branch != existing_branch:
                CartItem.objects.filter(cart=cart).delete()
                cartitems.clear()
        if any(item['branch'] != new_branch for item in ordercart):
            raise ValidationError({'error':'all items must be from same restaurant'})
        
        new_cartitems=[]
        for item in ordercart:
            product_id=item['product'].id
            if product_id in cartitems:
                existing_cartitem=cartitems[product_id]
                existing_cartitem.quantity+=item.get('quantity',1)
                existing_cartitem.branch=item['branch']
                existing_cartitem.save() 
            else:
                new_cartitems.append(CartItem(cart=cart,**item))

        if new_cartitems:
            CartItem.objects.bulk_create(new_cartitems)

        return cart

def update_cart(user,instance,validated_data):
    if user != instance.customer:
        raise serializers.ValidationError({'error':'you are not allowed to update this cart'})
    
    ordercart=validated_data.get("ordercart") #python dictionary type
    if  not ordercart:
        raise serializers.ValidationError({'error':'cart is empty'})
    
    ordercart_prod_ids={item['product'].id: item for item in ordercart}
    cartitems=CartItem.objects.filter(cart=instance.id)
    for cartitem in cartitems:
        if cartitem.product.id not in ordercart_prod_ids:
            cartitem.delete()

    for item in ordercart:
        try:
            product_id=item['product'].id
            quantity=item.get('quantity',1)
            branch=item['branch']
            if quantity <=0:
                raise serializers.ValidationError({'error':'quantity should be atleast 1'})
            cartitem=CartItem.objects.get(cart=instance.id,product=product_id)
            cartitem.quantity=quantity
            cartitem.save()
            
        except:
            CartItem.objects.create(
                cart=instance.id,
                branch=branch,
                product=item['product'],
                quantity=item.get('quantity',1))
            
    return instance