from django.db import models
from django.contrib.postgres.fields import ArrayField
# Create your models here.

shipping = (('0', 'Free'), ('5', '5 %'), ('10', '10 %'), ('20', '20 %'))

class Category(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Seller(models.Model):    
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=500)
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):  # __unicode__ on Python 2
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="static/images/", null=True, blank=True, max_length=500)
    price = models.DecimalField(max_digits=7, decimal_places=2, default=0.0)
    category = models.ForeignKey(Category)
    dimensions = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    shipping_details = models.CharField(max_length=10, choices=shipping, help_text='Select the shipping details for this Product', default='0')
    sold_by = models.ForeignKey(Seller)
    created_date = models.DateTimeField(auto_now_add = True)
    def __str__(self):  # __unicode__ on Python 2
        return self.name

