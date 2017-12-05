# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-05 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0017_auto_20171019_1750'),
    ]

    operations = [
        migrations.AddField(
            model_name='country',
            name='string_representation',
            field=models.TextField(blank=True, help_text='The string representation of this object', null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='string_representation',
            field=models.TextField(blank=True, help_text='The string representation of this object', null=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='string_representation',
            field=models.TextField(blank=True, help_text='The string representation of this object', null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='string_representation',
            field=models.TextField(blank=True, help_text='The string representation of this object', null=True),
        ),
        migrations.AddField(
            model_name='tourofduty',
            name='string_representation',
            field=models.TextField(blank=True, help_text='The string representation of this object', null=True),
        ),
    ]
