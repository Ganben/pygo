from __future__ import unicode_literals

from django.db import models
import datetime
import time
from uuid import uuid1
import os
from django.utils.dateformat import format
from django.utils.encoding import python_2_unicode_compatible
# from smartfields import fields
# from smartfields.dependencies import FileDependency
# from smartfields.processors import ImageProcesso

# Create your models here.
def pic_name(instance, filename):   #this method must be def before class, otherwise the class is doge
	ext = filename.split('.')[-1]
	# return '/'.join([str(datetime.date.year), '-', str(datetime.date.month), '/',  format(datetime.now(), u'U')])
#it should seperate year and month for archieve aspects need change! instance.user.domain, '-', instance.user.openid, '-',
	return 'pictures/{0}/{1}.{ext}'.format(time.strftime("%Y/%m/"), uuid1(), ext=ext)

@python_2_unicode_compatible
class User_p(models.Model):
	openid = models.CharField(max_length=40)
	domain = models.CharField(max_length=20, default='wechat')
	last_login = models.DateTimeField(blank=True)
	status = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.openid

@python_2_unicode_compatible
class Tag(models.Model):
	name = models.CharField(max_length=40)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

@python_2_unicode_compatible
class Pic(models.Model):
	# user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	user = models.CharField(max_length=50)    #lets try user with no db abs pic obj
	rated = models.IntegerField(default=0)
	rating = models.IntegerField(default=1500)
	# picture = models.ImageField(upload_to= 'pictures/%Y/%m')   #size limit is not permitted here.
	# picture = models.ImageField(upload_to=pic_name)
	picture = models.URLField(max_length=80)
	added = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=60)
	# tag = models.CharField(max_length=40, default=None)
	tag = models.ForeignKey(Tag, on_delete=models.DO_NOTHING)
	# should use foreignKey?

	def __str__(self):
		return self.text
	def addRate(self):
		self.rated += 1
	# def pic_name(self):
	# 	return '/'.join([str(datetime.date.year), '-', str(datetime.date.month), '/', self.user.domain, '-',
	# 					 self.user.openid, '-', format(datetime.now(), u'U')])



