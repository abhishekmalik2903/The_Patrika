# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-27 21:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0012_auto_20160831_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='firends2',
            field=models.ManyToManyField(blank=True, null=True, to='chat.Profile'),
        ),
    ]
