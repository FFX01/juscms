# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-17 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0006_auto_20160117_0157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='page',
            name='path',
            field=models.CharField(blank=True, max_length=800, verbose_name='Page URL Path'),
        ),
    ]
