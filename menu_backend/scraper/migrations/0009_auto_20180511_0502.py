# Generated by Django 2.0.5 on 2018-05-11 05:02

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0008_auto_20180511_0442'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hour',
            name='hours',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
