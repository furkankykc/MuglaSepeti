# Generated by Django 3.0.8 on 2020-10-06 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0004_collation_collationlist_collationnode'),
    ]

    operations = [
        migrations.AddField(
            model_name='collationnode',
            name='is_changed',
            field=models.BooleanField(default=False, verbose_name='is changed'),
        ),
        migrations.AddField(
            model_name='entry',
            name='collation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.CollationList', verbose_name='collation'),
        ),
        migrations.AlterField(
            model_name='collation',
            name='name',
            field=models.CharField(max_length=40, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='collation',
            name='price',
            field=models.FloatField(verbose_name='Price'),
        ),
        migrations.AlterField(
            model_name='collationlist',
            name='collation_list',
            field=models.ManyToManyField(to='muglaSepetiApp.CollationNode', verbose_name='Collation List'),
        ),
        migrations.AlterField(
            model_name='collationlist',
            name='name',
            field=models.CharField(max_length=20, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='collationnode',
            name='collation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.Collation', verbose_name='Collation'),
        ),
    ]
