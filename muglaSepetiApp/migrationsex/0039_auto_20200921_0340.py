# Generated by Django 3.0.8 on 2020-09-21 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0038_auto_20200921_0250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='comment'),
        ),
    ]