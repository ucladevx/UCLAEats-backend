# Generated by Django 2.0.5 on 2018-05-10 22:22

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0005_recipe'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='nutrition',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
        migrations.AlterField(
            model_name='activitylevel',
            name='level',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
