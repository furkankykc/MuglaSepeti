# Generated by Django 3.0.8 on 2020-08-26 13:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0016_auto_20200817_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='bucket',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.Bucket', verbose_name='Bucket'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='detail',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='detail'),
        ),
        migrations.AlterField(
            model_name='entry',
            name='name',
            field=models.CharField(max_length=50, verbose_name='name'),
        ),
    ]