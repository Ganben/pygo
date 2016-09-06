from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

from django.utils import timezone
import datetime
# Create your models here.

@python_2_unicode_compatible
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    #customized method
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - \
                                datetime.timedelta(days=1)

@python_2_unicode_compatible
class Choice(models.Model):
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text



# parking position
@python_2_unicode_compatible
class Position(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=40)
    section = models.CharField(max_length=40, default='A')
    # class Meta:
    #     ordering = ('section')

    def __str__(self):
        return self.name

    def start_parking(self, user):
        res = Parking()
        res.position = self
        res.user = user

        return res

#parking
@python_2_unicode_compatible
class Parking(models.Model):
    position = models.ForeignKey(
        Position, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    user = models.CharField(max_length=40, blank=False, default='test')
    manager = models.CharField(max_length=40, blank=True, default='')
    confirmby = models.CharField(max_length=40, blank=True, default='')
    isend = models.BooleanField(default=False)
    userend = models.BooleanField(default=False)
    starttime = models.DateTimeField('start', default=timezone.now)
    def __str__(self):
        return self.user

    def end_parking(self):
        self.isend = True
        self.save()
        return True
    # class Meta:
    #     ordering = ('created')

#billing
# @python_2_unicode_compatible
class Billing(models.Model):
    parking = models.ForeignKey(Parking,
                                 on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    charger = models.CharField(max_length=40, default='')
    paystatus = models.BooleanField(default=False)
    def __str__(self):
        return str(self.amount)

    def makepaid(self):
        if self.paystatus == False:
            self.paystatus = True
            return True

    # class Meta:
    #     ordering = ('paystatus')