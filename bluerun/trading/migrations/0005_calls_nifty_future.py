# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-17 17:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trading', '0004_calls_option_calls_uncovered'),
    ]

    operations = [
        migrations.AddField(
            model_name='calls',
            name='nifty_future',
            field=models.BooleanField(default=False),
        ),
    ]
