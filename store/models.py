from django.conf import settings
from django.db import models

# Create your models here.

#items that can be purchased
class Item(models.Model):
    
    title=models.CharField(max_length=100)
    price=models.FloatField()
    
    def __str__(self):
        return self.title
    

#items in the cart
class OrderItem(models.Model):
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

#cart
class Order(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items=models.ManyToManyField(OrderItem)
    start_date=models.DateTimeField(auto_now_add=True)
    order_date=models.DateTimeField()
    ordered=models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username