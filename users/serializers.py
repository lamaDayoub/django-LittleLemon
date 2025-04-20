from rest_framework import serializers
from django.contrib.auth.models import User, Group
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
       # help_text="The password for the user. It will be hashed before storage."
    )

    
    class Meta:
        model=User
        fields=['id','username','email','password']
       # extra_kwargs = {
        #    'username': {'help_text': 'The username for the user.'},
        #    'email': {'help_text': 'The email address for the user.'},
       
       
       # }
      
    
    def create(self, validated_data):
        # Create the user
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        
        # Add the user to the 'Customer' group
        customer_group = Group.objects.get(name='Customers')
        user.groups.add(customer_group)
        
        return user
    
class CustomerListSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
    
        ]
        read_only_fields = fields 