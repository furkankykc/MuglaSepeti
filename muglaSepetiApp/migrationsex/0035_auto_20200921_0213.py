# Generated by Django 3.0.8 on 2020-09-20 23:13

from django.db import migrations, models
import muglaSepetiApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0034_auto_20200921_0210'),
    ]

    operations = [
        migrations.RenameField(
            model_name='config',
            old_name='aboutus_description',
            new_name='about_description',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='aboutus_title',
            new_name='about_title',
        ),
        migrations.AddField(
            model_name='config',
            name='about_image_1',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, verbose_name='Slider Image 4'),
        ),
        migrations.AddField(
            model_name='config',
            name='about_image_2',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, verbose_name='Slider Image 4'),
        ),
        migrations.AddField(
            model_name='config',
            name='about_image_3',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, verbose_name='Slider Image 4'),
        ),
    ]