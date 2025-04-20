from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
# Create your models here.
class Cart(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="cartuser")
    menuitem=models.ForeignKey(MenuItem,on_delete=models.CASCADE,related_name="menuitemcart")
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField( max_digits=6, decimal_places=2)
    price=models.DecimalField(max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together=('menuitem','user')

