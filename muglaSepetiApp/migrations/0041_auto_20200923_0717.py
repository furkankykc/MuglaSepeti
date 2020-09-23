# Generated by Django 3.0.8 on 2020-09-23 04:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0040_auto_20200921_0407'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='service_delay',
            field=models.DurationField(default=datetime.timedelta(seconds=1800), verbose_name='Service Delay'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='config',
            name='about_content_description',
            field=models.CharField(blank=True, max_length=500, null=True, verbose_name='Content Description'),
        ),
        migrations.AlterField(
            model_name='config',
            name='about_fact_value_2',
            field=models.IntegerField(blank=True, null=True, verbose_name='Statistic Value 2'),
        ),
        migrations.AlterField(
            model_name='config',
            name='about_fact_value_3',
            field=models.IntegerField(blank=True, null=True, verbose_name='Statistic Value 3'),
        ),
        migrations.AlterField(
            model_name='config',
            name='about_fact_value_4',
            field=models.IntegerField(blank=True, null=True, verbose_name='Statistic Value 4'),
        ),
    ]
