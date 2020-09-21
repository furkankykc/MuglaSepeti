# Generated by Django 3.0.8 on 2020-09-20 23:08

from django.db import migrations, models
import muglaSepetiApp.models


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0031_auto_20200921_0146'),
    ]

    operations = [
        migrations.RenameField(
            model_name='config',
            old_name='breadcrumbBackground',
            new_name='bread_crumb_background',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='contentDescription',
            new_name='content_description',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='menuBackground',
            new_name='menu_background',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='menuInnerBackground',
            new_name='menu_inner_background',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='siteDescription',
            new_name='site_description',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderDescription',
            new_name='slider_description',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderImage1',
            new_name='slider_image_1',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderImage2',
            new_name='slider_image_2',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderImage3',
            new_name='slider_image_3',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderImage4',
            new_name='slider_image_4',
        ),
        migrations.RenameField(
            model_name='config',
            old_name='sliderTitle',
            new_name='slider_title',
        ),
        migrations.AddField(
            model_name='config',
            name='aboutus_description',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
        migrations.AddField(
            model_name='config',
            name='aboutus_title',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='config',
            name='footer_logo',
            field=models.ImageField(blank=True, null=True, upload_to=muglaSepetiApp.models.get_image_path, verbose_name='Footer Logo'),
        ),
    ]
