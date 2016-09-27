from __future__ import unicode_literals

from django.db import models
import datetime
from uuid import uuid1
import os
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
	# user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
	user = models.CharField(max_length=50)    #lets try user with no db abs pic obj
	rated = models.IntegerField(default=0)
	rating = models.IntegerField(default=1500)
	picture = models.ImageField(upload_to= 'pictures/%Y/%m')   #size limit is not permitted here.
	# picture = models.FilePathField()
	added = models.DateTimeField(auto_now_add=True)
	text = models.CharField(max_length=60)
	tag = models.CharField(max_length=40, default=None)
	# should use foreignKey?

	def __str__(self):
		return str(self.rating)
	def addRate(self):
		self.rated += 1
	# def pic_name(self):
	# 	return '/'.join([str(datetime.date.year), '-', str(datetime.date.month), '/', self.user.domain, '-',
	# 					 self.user.openid, '-', format(datetime.now(), u'U')])

class Tag(models.Model):
	name = models.CharField(max_length=40)
	active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return self.name

def pic_name(instance, filename):
	# return '/'.join([str(datetime.date.year), '-', str(datetime.date.month), '/',  format(datetime.now(), u'U')])
#it should seperate year and month for archieve aspects need change! instance.user.domain, '-', instance.user.openid, '-',
	return '.{0}/{1}/{2}_{file}'.format(str(datetime.date.year), str(datetime.date.month), uuid1(), file=filename)