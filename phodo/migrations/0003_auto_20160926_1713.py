# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 09:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('phodo', '0002_auto_20160926_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='picture',
            field=models.ImageField(height_field=800, upload_to="<attribute 'year' of 'datetime.date' objects>/<attribute 'month' of 'datetime.date' objects>/<type 'datetime.time'>", width_field=1600),
        ),
    ]
