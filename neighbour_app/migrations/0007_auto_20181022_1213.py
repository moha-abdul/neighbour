# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-10-22 09:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('neighbour_app', '0006_auto_20181022_1122'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='location',
            field=models.CharField(max_length=60, null=True),
        ),
        migrations.AlterField(
            model_name='posts',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Posts', to=settings.AUTH_USER_MODEL),
        ),
    ]
