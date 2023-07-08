from rest_framework import serializers
from .models import Cart, WishList


class CartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Cart
        fields = '__all__'


class WishSerializer(serializers.ModelSerializer):

    class Meta:
        model = WishList
        fields = '__all__'
