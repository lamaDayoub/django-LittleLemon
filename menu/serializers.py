from rest_framework import serializers
from .models import MenuItem,Category
import bleach



class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields=['id','slug','title']
    def validate_title(self,value):
        return bleach.clean(value)
        
class MenuItemsSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = MenuItem
        fields = ['id','title', 'price', 'featured', 'category_id', 'category']

    def validate_title(self, value):
        return bleach.clean(value)

    def create(self, validated_data):
        # Fetch the category object using category_id
        category_id = validated_data.pop('category_id')
        category = Category.objects.get(id=category_id)

        # Create the MenuItem
        item = MenuItem.objects.create(
            title=validated_data['title'],
            price=validated_data['price'],
            featured=validated_data['featured'],
            category=category  # Assign the fetched category object
        )

        return item