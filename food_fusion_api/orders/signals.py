# from django.dispatch import receiver
# from django.db.models.signals import post_save,post_delete
# from .models import Checkout
# from .serializers import CartCreateSerializer
# import logging

# logger=logging.getLogger(__name__)

# @receiver(post_save,sender=Checkout)
# def create_branch(sender,instance,created,**kwargs):
#     try:
#         if created:
#             cart=instance.cart
#             if cart:
#                 instance._cart_data=CartCreateSerializer(cart).data
#                 cart.delete()
#                 print("cart has been deleted")
#             else:
#                 logger.error(f"no cart exist")
#     except Exception as e:
#         logger.error(f'signal has error: {e}')
# # @receiver(post_delete,sender=Address)
# # def delete_branch(sender,instance,**kwargs):
# #     Branch.objects.filter(address_id=instance).delete()

