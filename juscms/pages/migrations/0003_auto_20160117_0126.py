# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-17 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20160117_0124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='position',
        ),
        migrations.RemoveField(
            model_name='row',
            name='position',
        ),
    ]
