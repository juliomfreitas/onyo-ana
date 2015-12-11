# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-11 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('powerball_checker', '0003_prize_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='code',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ticket',
            name='winning',
            field=models.NullBooleanField(),
        ),
    ]
