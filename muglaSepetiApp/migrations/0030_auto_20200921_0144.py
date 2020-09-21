# Generated by Django 3.0.8 on 2020-09-20 22:44

import django.core.validators
from django.db import migrations, models
import muglaSepetiApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0029_auto_20200921_0037'),
    ]

    operations = [
        migrations.AddField(
            model_name='config',
            name='favicon',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['ico'])], verbose_name='icon'),
        ),
        migrations.AlterField(
            model_name='config',
            name='breadcrumbBackground',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])], verbose_name='Breadcrumb Background'),
        ),
        migrations.AlterField(
            model_name='config',
            name='menuBackground',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])], verbose_name='Menu Background'),
        ),
        migrations.AlterField(
            model_name='config',
            name='menuInnerBackground',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png'])], verbose_name='Menu Inner Background'),
        ),
    ]
