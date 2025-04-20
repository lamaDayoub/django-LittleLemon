from rest_framework import serializers
from .models import Cart, MenuItem
from django.contrib.auth.models import User

class SafeCurrentUserDefault(serializers.CurrentUserDefault):
    def __call__(self, field):
        try:
            return super().__call__(field)  # Works in real requests
        except (KeyError, AttributeError):
            return None  # Skip during Swagger schema generation
class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        default=SafeCurrentUserDefault(),  # 👈 Use the safe version
        read_only=False,  # Allow Swagger to see it (but it won't break)
    )
    menuitem=serializers.PrimaryKeyRelatedField(
        queryset=MenuItem.objects.all()
    )
    class Meta:
        model=Cart
        fields=['id','user','menuitem','quantity','unit_price','price']
        read_only_fields = ['id', 'user', 'unit_price', 'price']
    def validate_quantity(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value
    def create(self, validated_data):
        # Calculate unit_price and price based on the menu item
        menuitem = validated_data['menuitem']
        validated_data['unit_price'] = menuitem.price
        validated_data['price'] = menuitem.price * validated_data['quantity']

        # Ensure the user is set to the current authenticated user
        validated_data['user'] = self.context['request'].user

        return super().create(validated_data)