# Generated by Django 3.0.8 on 2020-08-12 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0003_auto_20200812_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='checked_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='delivered_at',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='is_deleted',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='is_delivered',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='ordered_at',
            field=models.DateTimeField(blank=True),
        ),
    ]