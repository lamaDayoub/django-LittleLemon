from django.db import models
from django.contrib.auth.models import User
from menu.models import MenuItem
from django.utils import timezone
# Create your models here.
class Order(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="orderer")
    delivery_crew=models.ForeignKey(User, on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status=models.BooleanField(db_index=True,default=0)
    total=models.DecimalField( max_digits=6, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return f"Order {self.id} by {self.user.username}"
class OrderItem(models.Model):
    order=models.ForeignKey(Order, on_delete=models.CASCADE,related_name='order_items')
    menuitem=models.ForeignKey(MenuItem, on_delete=models.CASCADE,related_name="menuitem")
    quantity=models.SmallIntegerField()
    unit_price=models.DecimalField( max_digits=6, decimal_places=2)
    price=models.DecimalField( max_digits=6, decimal_places=2)
    
    class Meta:
        unique_together=('order','menuitem')
    def __str__(self):
        return f"{self.quantity} x {self.menuitem.title} (Order: {self.order.id})"
