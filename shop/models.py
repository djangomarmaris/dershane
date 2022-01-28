import os
from PIL import Image, ExifTags
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models
from django.urls import reverse
from embed_video.fields import EmbedVideoField
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    parent = models.ForeignKey('self',blank=True,null=True,related_name='inside_category',on_delete=models.CASCADE)
    name = models.CharField(max_length=20, db_index=True)
    slug = models.SlugField(max_length=20, db_index=True, unique=True)

    class Meta:
        unique_together =('slug','parent')
        verbose_name_plural = 'categories'


    def __str__(self):
        full_path = [self.name]

        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return '->'.join(full_path[::-1])



    def get_absolute_url(self):
        return reverse('shop:product_list_by_show', args=[self.slug])



class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete = models.CASCADE)
    product_no = models.CharField(max_length=25,default='Ürün Kodu Giriniz')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    info = RichTextUploadingField()
    video = EmbedVideoField()
    description = RichTextUploadingField(blank=True)
    shop = RichTextUploadingField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=0)
    normal_price = models.CharField(max_length=4,db_index=True,default='SOME STRING')
    discount = models.CharField(max_length=4,db_index=True,default='SOME STRING')
    stock = models.PositiveIntegerField()
    noDropDown = models.BooleanField(blank=True)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    seo = models.CharField(max_length=500,default="Seo için Bilgi Giriniz.")
    key = models.CharField(max_length=550,default="Keyword için Giriş")


    class Meta:
        ordering = ('created',)
        index_together = (('id', 'slug',))

    def __str__(self):
        return self.name


    def get_cat_list(self):
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb)-1):
            breadcrumb[i]='/'.join(breadcrumb[-1:i-1:-1])
        return breadcrumb[-1:0:-1]



    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])






