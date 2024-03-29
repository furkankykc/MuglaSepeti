# Generated by Django 3.0.8 on 2020-10-06 21:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('muglaSepetiApp', '0005_auto_20201006_1924'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='collationnode',
            name='is_changed',
        ),
        migrations.CreateModel(
            name='BucketCollation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.CollationList')),
                ('collation_list', models.ManyToManyField(to='muglaSepetiApp.CollationNode', verbose_name='Collation List')),
            ],
        ),
        migrations.AddField(
            model_name='bucketentry',
            name='collation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='muglaSepetiApp.BucketCollation'),
        ),
    ]
