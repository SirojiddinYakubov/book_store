from datetime import datetime, timezone

from django.db import models
from django.utils.translation import gettext_lazy as _

from common.models import (BaseModel, Category, Store)
from conf import settings


def book_image_upload_path():
    dtnow = datetime.now(timezone.utc)
    dtstr = '{:%Y/%m/%d}'.format(dtnow)
    dtstr = 'images/books/' + dtstr
    return dtstr


class Book(BaseModel):
    """ Книга """
    title = models.CharField(verbose_name=_('Название'), max_length=100)
    category = models.ForeignKey(Category, verbose_name=_('Категория'), on_delete=models.CASCADE)
    store = models.ForeignKey(Store, verbose_name=_('Магазин'), on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_('Изображение'), upload_to=book_image_upload_path())
    desc = models.CharField(verbose_name=_('Описание'), max_length=255)
    author = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_('Автор'))
    pub_date = models.DateField(verbose_name=_('Дата публикации'))

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"




