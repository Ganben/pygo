from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.

@python_2_unicode_compatible
class Item(models.Model):
    name = models.CharField(max_length=40)
    phone = models.CharField(max_length=30)
    date = models.CharField(max_length=20)
    is1 = models.BooleanField(default=False)
    is2 = models.BooleanField(default=False)
    is3 = models.BooleanField(default=False)
    number = models.IntegerField(null=True)
    def __str__(self):
        s = "-"
        seq = (self.name, str(self.number))
        return s.join(seq)
