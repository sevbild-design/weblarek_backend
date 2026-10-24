import uuid

from django.core.validators import MinValueValidator
from django.db import models, transaction


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


class OrderCounter(models.Model):
    last_number = models.PositiveBigIntegerField(default=0)


class Order(models.Model):
    class PaymentChoices(models.TextChoices):
        CARD = 'card', 'Картой'
        CASH = 'cash', 'Наличными'

    id = models.CharField(
        primary_key=True,
        max_length=36,
        editable=False,
    )
    number = models.PositiveBigIntegerField(
        unique=True,
        editable=False,
    )
    payment = models.CharField(
        verbose_name='Способ оплаты',
        max_length=4,
        choices=PaymentChoices.choices,
    )
    email = models.EmailField(
        verbose_name='email',
        max_length=30
    )
    phone = models.CharField(
        verbose_name='Номер телефона',
        max_length=20
    )
    address = models.CharField(
        verbose_name='Адрес доставки',
        max_length=255
    )
    total = models.PositiveIntegerField(
        verbose_name='Стоимость заказа',
    )
    items = models.ManyToManyField(
        Products,
        verbose_name='Товары в заказе',
        related_name='orders'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = str(uuid.uuid4())
        if self._state.adding:
            with transaction.atomic():
                counter = (
                    OrderCounter.objects
                    .select_for_update()
                    .get(pk=1)
                )

                counter.last_number += 1
                counter.save(update_fields=['last_number'])

                self.number = counter.last_number

                return super().save(*args, **kwargs)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.number}'
