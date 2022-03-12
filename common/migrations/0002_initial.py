# Generated by Django 4.0.2 on 2022-03-12 17:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0002_initial'),
        ('common', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь'),
        ),
        migrations.AddField(
            model_name='product',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book', verbose_name='Книга'),
        ),
        migrations.AddField(
            model_name='product',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавивший товар на склад'),
        ),
        migrations.AddField(
            model_name='product',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='orderedproduct',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book', verbose_name='Книга'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_customer', to=settings.AUTH_USER_MODEL, verbose_name='Клиент'),
        ),
        migrations.AddField(
            model_name='order',
            name='ordered_product',
            field=models.ManyToManyField(to='common.OrderedProduct', verbose_name='Заказанные продукты'),
        ),
        migrations.AddField(
            model_name='order',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='order',
            name='supplier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='order_supplier', to=settings.AUTH_USER_MODEL, verbose_name='Поставщик'),
        ),
        migrations.AddField(
            model_name='importproduct',
            name='book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='book.book', verbose_name='Книга'),
        ),
        migrations.AddField(
            model_name='importproduct',
            name='store',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.store', verbose_name='Магазин'),
        ),
        migrations.AddField(
            model_name='discount',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь, добавивший скидка на товар'),
        ),
        migrations.AddField(
            model_name='discount',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.product', verbose_name='Товар'),
        ),
        migrations.AddField(
            model_name='acceptpayment',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.order', verbose_name='Заказ'),
        ),
        migrations.AddField(
            model_name='acceptorder',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='common.order', verbose_name='Заказ'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.CheckConstraint(check=models.Q(('rate__range', (0, 5))), name='valid_rate'),
        ),
        migrations.AddConstraint(
            model_name='rating',
            constraint=models.UniqueConstraint(fields=('user', 'book'), name='rating_once'),
        ),
    ]
