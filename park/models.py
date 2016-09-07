from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
import datetime
# Create your models here.

@python_2_unicode_compatible
class Car(models.Model):
    name = models.CharField(max_length=20)


@python_2_unicode_compatible
class Ticket(models.Model):
    car = models.ForeignObject(Car, validators=True)    #any way, many to one? not sure;
    starttime = models.DateTimeField('start')
    zone = models.DecimalField()   #GPS
    fee_rate = models.IntegerField()
    duration = models.DurationField()  #can be extended via extend
    charger = models.CharField(max_length=10)   #who created
    ispaid = models.BooleanField()    # if is paid
    # billing = models.ManyToOneRel(Billing, validate=False)   #if paid, the billing must match? problem to paid.

class Billing(models.Model):
    amount = models.IntegerField
    ticket = models.ForeignKey(Ticket)
    transaction = models.CharField(max_length=40)
