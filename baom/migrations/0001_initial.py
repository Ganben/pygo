# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-12 07:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40)),
                ('phone', models.CharField(max_length=30)),
                ('date', models.CharField(max_length=20)),
                ('is1', models.BooleanField(default=False)),
                ('is2', models.BooleanField(default=False)),
                ('is3', models.BooleanField(default=False)),
                ('number', models.IntegerField()),
            ],
        ),
    ]
