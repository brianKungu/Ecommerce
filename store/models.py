from django.conf import settings
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField

# Create your models here.

CATEGORY_CHOICE=(
    ('S','Shirt'),
    ('SH','Shoe'),
    ('SW','Sport wear'),
    ('OW','Outwear')
)

CATEGORY_LABEL=(
    ('P','primary'),
    ('S','secondary'),
    ('D','danger')
)

#items that can be purchased
class Item(models.Model):
    
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICE, max_length=2)
    label = models.CharField(choices=CATEGORY_LABEL, max_length=2)
    slug = models.SlugField()
    description = models.TextField()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('store:product', kwargs={
            'slug': self.slug
        })
        
    def get_add_to_cart_url(self):
        return reverse('store:add_to_cart', kwargs={
            'slug': self.slug
        })
    
    def remove_from_cart_url(self):
        return reverse('store:remove_from_cart', kwargs={
            'slug':self.slug
        })

#items in the cart
class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE , blank=True ,null=True)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    
     
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    
    def get_total_item_price(self):
        return self.quantity * self.item.price
    
    def get_total_discount_price(self):
        return self.quantity * self.item.discount_price
    
    def get_amount_saved(self):
        return self.get_total_item_price() - self.get_total_discount_price()

    def get_final_amount(self):
        if self.item.discount_price:
            return self.get_total_discount_price()
        return self.get_total_item_price()
            
#cart
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    
    def __str__(self):
        return self.user.username
    
    def get_total(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_amount()
        return total
    

class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip =models.CharField(max_length=100) 
    def __str__(self):
        return self.user.username
    
class Payment(models.Model):
     stripe_charge_id = models.CharField(max_length=50)
     user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
     amount = models.FloatField()
     timestamp = models.DateField(auto_now=True)
     
     def __str__(self):
         return self.user.username
     