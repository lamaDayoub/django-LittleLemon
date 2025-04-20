from rest_framework import serializers
from cart.models import Cart, MenuItem
from django.contrib.auth.models import User
from .models import Order,OrderItem

class OrderItemSerializer(serializers.ModelSerializer):
    menuitem=serializers.PrimaryKeyRelatedField(queryset=MenuItem.objects.all())
    class Meta:
        model=OrderItem
        fields = [ 'id','order', 'menuitem', 'quantity', 'unit_price', 'price']
        read_only_fields = [ 'order', 'unit_price', 'price']

class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user' , 'status' , 'delivery_crew','total', 'created_at', 'updated_at', 'order_items']
        read_only_fields = [ 'user', 'status', 'delivery_crew','total', 'created_at', 'updated_at']