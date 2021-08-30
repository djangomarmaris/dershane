# Generated by Django 3.0.5 on 2021-07-24 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='tc',
            field=models.CharField(default=24, max_length=11, verbose_name='Tc No:'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='uniqid',
            field=models.CharField(default=24, max_length=11, verbose_name='Uniq id:'),
            preserve_default=False,
        ),
    ]
