# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-10-11 05:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pyteams', '0003_auto_20161009_0853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='team',
            name='name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterUniqueTogether(
            name='team',
            unique_together=set([('name', 'team_type')]),
        ),
    ]
