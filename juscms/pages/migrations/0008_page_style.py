# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-20 04:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0007_auto_20160117_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='style',
            field=models.TextField(blank=True, verbose_name='Page Specific CSS'),
        ),
    ]