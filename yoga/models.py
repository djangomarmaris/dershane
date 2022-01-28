from django.db import models

# Create your models here.


class kvvk(models.Model):
    name = models.CharField(max_length=200, db_index=True,default='Açıklama Başlığı',verbose_name='Name')
    kvvk = models.FileField(upload_to='products/katalog/%y/%m/%d')

    def __str__(self):
        return self.name




class Documents(models.Model):
    name = models.CharField(max_length=200, db_index=True, default='Açıklama Başlığı', verbose_name='Name')
    image = models.ImageField(upload_to='products/%y/%m/%d', blank=True)
    document = models.FileField(upload_to='products/katalog/%y/%m/%d')


    def __str__(self):
        return self.name


class Exam(models.Model):
    name = models.CharField(max_length=100,default='Öğrenci')
    paper = models.FileField(upload_to='products/%y/%m/%d')

    def __str__(self):
        return self.name