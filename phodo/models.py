from __future__ import unicode_literals

from django.db import models
import datetime
from django.utils.dateformat import format

# Create your models here.
class User(models.Model):
	openid = models.CharField(max_length=40)
	domain = models.CharField(max_length=20, default='wechat')
	last_login = models.DateTimeField()
	status = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.openid

class Pic(models.Model):
	user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	rated = models.IntegerField(default=0)
	rating = models.IntegerField(default=1500)
	picture = models.ImageField(upload_to=pic_name)
	added = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=60)
	def __str__(self):
		return self.picture

def pic_name(instance):
	return '/'.join([str(datetime.date.year), '-', str(datetime.date.month), '/', instance.user.domain, '-', instance.user.openid, '-', format(datetime.now(), u'U')])
#it should seperate year and month for archieve aspects need change!
