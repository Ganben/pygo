from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
import datetime
# Create your models here.

@python_2_unicode_compatible
class Car(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Ticket(models.Model):
    car = models.ForeignKey(Car, validators=True)    #any way, many to one? not sure;
    starttime = models.DateTimeField('start')
    zone = models.CharField(max_length=40)   #GPS
    fee_rate = models.IntegerField()
    duration = models.DurationField()  #can be extended via extend
    charger = models.CharField(max_length=10)   #who created
    ispaid = models.BooleanField()    # if is paid
    # billing = models.ManyToOneRel(Billing, validate=False)   #if paid, the billing must match? problem to paid.
    def __str__(self):
        return self.zone


class Billing(models.Model):
    amount = models.IntegerField
    ticket = models.ForeignKey(Ticket)
    transaction = models.CharField(max_length=40)

    def __str__(self):
        return self.ticket

class User(models.Model):
    name = models.CharField(max_length=40)
    openid = models.CharField(max_length=40, default=None)
    domain = models.CharField(max_length=40, default='wechat')
    def __str__(self):
        return self.name

class Picture(models.Model):
    name = models.CharField(max_length=50)
    # picture = models.ImageField(upload_to= 'pictures')
    def __str__(self):
        return self.name
    

