import uuid

from django.core.validators import MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(
        verbose_name='Название',
        max_length=100,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Products(models.Model):

    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    # image = models.ImageField(
    #     verbose_name='Изображение',
    #     upload_to='products/images/'
    # )
    image = models.CharField(
        verbose_name='Изображение',
        max_length=100,
    )
    title = models.CharField(
        verbose_name='Название',
        max_length=100,
    )
    category = models.ForeignKey(
        Category,
        verbose_name='Категория',
        on_delete=models.CASCADE,
    )
    price = models.PositiveIntegerField(
        verbose_name='Цена',
        validators=[MinValueValidator(0)],
        blank=True,
        null=True
    )

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'
        default_related_name = 'products'

    def __str__(self):
        return self.title
