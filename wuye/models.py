#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.db import models
# gen a house item list page; contains normal tags of a immobile assets.
# think about management roles;

# Create your models here.

@python_2_unicode_compatible
class Item(models.Model):
    addr = models.CharField(max_length=60)
    city = models.CharField(max_length=40) #consider a existed enum?
    province = models.CharField(max_length=40) #a existed collection?
    dist = models.CharField(max_length=40)
    street = models.CharField(max_length=60)
    resblock = models.CharField(max_length=100) #free defined and should fuzzy match
    pic = models.URLField(max_length=60)    #use oss too
    added = models.DateTimeField(auto_now_add=True)
