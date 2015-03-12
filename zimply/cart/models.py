from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
# Create your models here.

class cart(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    cart_details = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    def __str__(self):  # __unicode__ on Python 2
        return self.name.username
