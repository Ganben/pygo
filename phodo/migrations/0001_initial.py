# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 08:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rated', models.IntegerField(default=0)),
                ('rating', models.IntegerField(default=1500)),
                ('picture', models.ImageField(upload_to="<attribute 'year' of 'datetime.date' objects>/<attribute 'month' of 'datetime.date' objects>/<type 'datetime.time'>")),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(max_length=60)),
                ('tag', models.CharField(default=None, max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.CharField(max_length=40)),
                ('domain', models.CharField(default='wechat', max_length=20)),
                ('last_login', models.DateTimeField()),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.AddField(
            model_name='pic',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='phodo.User'),
        ),
    ]
