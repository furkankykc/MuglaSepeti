# Generated by Django 3.0.8 on 2020-10-18 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0008_auto_20201017_2341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collation',
            name='name',
            field=models.CharField(max_length=40, unique=True, verbose_name='Name'),
        ),
    ]
