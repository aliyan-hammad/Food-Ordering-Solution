from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Address


class AddressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=Address
        fields=['id','address_lane1','address_lane2','country','city','town','latitude','longitude']


