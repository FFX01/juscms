# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-17 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20160117_0126'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='position',
            field=models.IntegerField(default=1, verbose_name='Position in Inline Admin'),
        ),
        migrations.AddField(
            model_name='row',
            name='position',
            field=models.IntegerField(default=0, verbose_name='Position in Inline Admin'),
        ),
    ]
