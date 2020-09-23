# Generated by Django 3.0.8 on 2020-08-13 19:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0005_auto_20200812_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='closed_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 13, 19, 21, 40, 403694, tzinfo=utc)),
        ),
        migrations.AddField(
            model_name='company',
            name='is_open',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='open_at',
            field=models.TimeField(default=datetime.datetime(2020, 8, 13, 19, 21, 40, 403676, tzinfo=utc)),
        ),
    ]
