# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-03-15 08:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20160207_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='categories',
            field=models.ManyToManyField(blank=True, related_name='items', to='main.ItemCategory', verbose_name='\u0532\u0561\u056a\u056b\u0576\u0576\u0565\u0580'),
        ),
    ]