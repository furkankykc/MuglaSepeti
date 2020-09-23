# Generated by Django 3.0.8 on 2020-09-20 14:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0020_company_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='menu',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.Company', verbose_name='Company'),
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Name'),
        ),
        migrations.CreateModel(
            name='PacketPrice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Address')),
                ('price', models.FloatField(default=5, verbose_name='Minimum Price')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.Company', verbose_name='Company')),
            ],
            options={
                'verbose_name': 'Minimum Packet Price',
                'verbose_name_plural': 'Minimum Packet Prices',
            },
        ),
    ]