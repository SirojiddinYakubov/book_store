from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import CheckConstraint, UniqueConstraint, Q
from django.utils.translation import gettext_lazy as _
from conf import settings


class BaseModel(models.Model):
    is_active = models.BooleanField(default=True, verbose_name=_('Активен'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата создания'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата обновления'))

    class Meta:
        abstract = True


class Store(BaseModel):
    """ Магазин """
    title = models.CharField(verbose_name=_('Название'), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"


class Category(BaseModel):
    """ Категория """
    title = models.CharField(verbose_name=_('Название'), max_length=255)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class ImportProduct(BaseModel):
    book = models.ForeignKey('book.Book', verbose_name=_('Книга'), on_delete=models.CASCADE)
    price = models.DecimalField(verbose_name=_('Цена'), max_digits=12, decimal_places=2)
    store = models.ForeignKey(Store, verbose_name=_("Магазин"), on_delete=models.CASCADE)
    count = models.PositiveIntegerField(verbose_name=_('Количество товаров'))

    def __str__(self):
        return "{0} : {1} : {2}".format(self.store, self.book, self.count)

    class Meta:
        verbose_name = "Добавить товар на склад"
        verbose_name_plural = "Добавить товар на склад"


class Product(BaseModel):
    """ Товар на складе """
    store = models.ForeignKey(Store, verbose_name=_("Магазин"), on_delete=models.CASCADE)
    book = models.ForeignKey('book.Book', verbose_name=_('Книга'), on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0, verbose_name=_('Количество товаров'))
    price = models.DecimalField(verbose_name=_('Цена'), max_digits=12, decimal_places=2)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь, добавивший товар на склад'),
                                   on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return "{0} : {1} : {2}".format(self.store, self.book, self.count)

    class Meta:
        verbose_name = "Товар на складе"
        verbose_name_plural = "Товар на складе"


class Order(BaseModel):
    """ Заказ """
    customer = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Клиент'), on_delete=models.SET_NULL,
                                 null=True,
                                 related_name='order_customer')
    supplier = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Поставщик'), on_delete=models.SET_NULL,
                                 null=True, blank=True,
                                 related_name='order_supplier')
    store = models.ForeignKey(Store, verbose_name=_("Магазин"), on_delete=models.CASCADE)
    ordered_product = models.ManyToManyField('OrderedProduct', verbose_name=_('Заказанные продукты'))
    place_of_delivery = models.CharField(verbose_name=_('Место доставки'), max_length=255, blank=True)


    def __str__(self):
        return "{0} {1}".format(self.customer, self.ordered_product.first())

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"


class OrderedProduct(BaseModel):
    book = models.ForeignKey('book.Book', verbose_name=_('Книга'), on_delete=models.CASCADE)
    count = models.PositiveSmallIntegerField(verbose_name=_('Количество товаров'))
    price = models.DecimalField(verbose_name=_('Цена'), max_digits=12, decimal_places=2)

    def __str__(self):
        return "{0} : {1}".format(self.book, self.count)


class Discount(BaseModel):
    """ Скидка """
    product = models.ForeignKey(Product, verbose_name=_('Товар'), on_delete=models.CASCADE)
    start_date = models.DateTimeField(verbose_name=_("Начало"))
    end_date = models.DateTimeField(verbose_name=_("Конец"))
    percent = models.FloatField(verbose_name=_('Процент скидки'))
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь, добавивший скидка на товар'),
                                   on_delete=models.SET_NULL, null=True)

    class Meta:
        verbose_name = "Скидка"
        verbose_name_plural = "Скидки"


class AcceptOrder(BaseModel):
    """ Принять заказ """
    order = models.ForeignKey(Order, verbose_name=_('Заказ'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Принять заказ"
        verbose_name_plural = "Принять заказы"


class AcceptPayment(BaseModel):
    """ Принимать платеж """

    class PaymentType(models.IntegerChoices):
        CASH_PAYMENT = 0, _('Наличный')
        PAYMENT_BY_CARD = 1, _('Оплата картой')

    order = models.ForeignKey(Order, verbose_name=_('Заказ'), on_delete=models.CASCADE)
    payment_type = models.IntegerField(verbose_name=_('Cпособ оплаты'), choices=PaymentType.choices)
    received_amount = models.DecimalField(verbose_name=_('Полученная сумма'), max_digits=12, decimal_places=2)

    class Meta:
        verbose_name = "Принимать платеж"
        verbose_name_plural = "Принимать платежи"


class Rating(BaseModel):
    """ Оценка """
    rate = models.FloatField(verbose_name=_('Оценка'), validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    book = models.ForeignKey("book.Book", verbose_name=_('Книга'), on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name=_('Пользователь'), on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"
        constraints = [
            CheckConstraint(check=Q(rate__range=(0, 5)), name='valid_rate'),
            UniqueConstraint(fields=['user', 'book'], name='rating_once')
        ]

    def __str__(self):
        return "{0} : {1} : {2}".format(self.user, self.book, self.rate)
