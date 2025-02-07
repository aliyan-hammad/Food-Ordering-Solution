from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Address
class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=Address
        fields=['id','address_lane1','address_lane2','country','city','town','latitude','longitude']

class UserAddressSerializer(serializers.ModelSerializer):
    edit_url=serializers.SerializerMethodField(read_only=True)
    url=serializers.HyperlinkedIdentityField(view_name='address-detail',lookup_field='id')
    class Meta():
        model=Address
        fields=['id','url','edit_url','address_lane1','address_lane2','country','city','town','latitude','longitude']

    def create(self,validated_data):
        user=self.context['request'].user
        address=Address.objects.create(
            entity_type='user',
            entity_id=user.id,
            **validated_data
        )
        return address
    def update(self,instance,validated_data):
        id=instance.id
        address_obj=Address.objects.get(id=id)
        for attr,value in validated_data.items():
            setattr(address_obj,attr,value)
        address_obj.save()
        return instance
    
    def get_edit_url(self,obj):
        request=self.context.get('request')
        return reverse('address-update', kwargs={'id':obj.id} , request=request)
    # def get_url(self,obj):
    #     request=self.context.get('request')
    #     return reverse('address-detail' , kwargs={'entity_type':obj.entity_type,'entity_id':obj.entity_id},request=request)
