from django.db import models


class Item(models.Model):
    title = models.CharField(max_length=30, verbose_name='наименование')
    description = models.TextField(max_length=200, verbose_name='описание')
    image = models.ImageField(verbose_name='картинка')
    weight = models.IntegerField(verbose_name='вес в граммах')
    price = models.DecimalField(decimal_places=2, max_digits=10, verbose_name='цена')

    def __str__(self):
        return str(self.title)
