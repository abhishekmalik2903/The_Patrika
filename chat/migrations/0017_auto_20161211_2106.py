# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-12-12 02:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0016_auto_20161206_1946'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ManyToManyField(to='chat.Profile'),
        ),
    ]
