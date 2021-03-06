# Generated by Django 3.0.5 on 2021-11-07 16:20

import ckeditor_uploader.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0004_auto_20210822_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_en',
            field=models.CharField(db_index=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='name_tr',
            field=models.CharField(db_index=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='description_tr',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='info_en',
            field=models.TextField(default='Ürün Aaçıklama', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='info_tr',
            field=models.TextField(default='Ürün Aaçıklama', null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_en',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='name_tr',
            field=models.CharField(db_index=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='shop_en',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='shop_tr',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True),
        ),
    ]
