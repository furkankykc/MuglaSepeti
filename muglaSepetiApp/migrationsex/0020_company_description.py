# Generated by Django 3.0.8 on 2020-09-17 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0019_auto_20200915_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='description',
            field=models.CharField(default=1, max_length=500, verbose_name='description'),
            preserve_default=False,
        ),
    ]
