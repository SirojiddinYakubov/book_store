import datetime

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from rest_framework import serializers

from api.v1.book.serializers import BookSerializer, BookShortSerializer
from api.v1.user.serializers import CustomUserShortSerializer
from book.models import Book
from common.models import (Category, Store, Product, ImportProduct, Discount, Rating, Order, OrderedProduct,
                           AcceptOrder, AcceptPayment)
from conf import settings

User = get_user_model()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title'
        ]


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            'id',
            'title'
        ]


class ProductSerializer(serializers.ModelSerializer):
    book = BookShortSerializer()
    store = StoreSerializer()
    created_by = CustomUserShortSerializer()

    class Meta:
        model = Product
        fields = [
            'id',
            'store',
            'book',
            'count',
            'created_by',
            'price'
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['book'] = BookShortSerializer(instance.book).data
        context['store'] = StoreSerializer(instance.store).data
        return context


class ImportProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImportProduct
        fields = [
            'id',
            'book',
            'price',
            'store',
            'count'
        ]

    def create(self, validated_data):
        store = validated_data.get('store')
        book = validated_data.get('book')
        price = validated_data.get('price')
        count = validated_data.get('count')

        obj = Product.objects.filter(book=book, store=store).last()
        user = self.context['request'].user
        if obj:
            obj.count += count
            obj.price = price
            obj.save()
        else:
            Product.objects.create(store=store, book=book, count=count, price=price, created_by=user)
        return super().create(validated_data)

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['book'] = BookShortSerializer(instance.book).data
        context['store'] = StoreSerializer(instance.store).data
        return context


class ImportProductSerializer(serializers.ModelSerializer):
    book = BookSerializer()
    store = StoreSerializer()

    class Meta:
        model = ImportProduct
        fields = [
            'id',
            'book',
            'price',
            'store',
            'count'
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['book'] = BookShortSerializer(instance.book).data
        return context


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            'id',
            'product',
            'start_date',
            'end_date',
            'percent',
            'created_by',
        ]
        extra_kwargs = {
            'created_by': {'required': True}
        }

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['product'] = ProductSerializer(instance.product).data
        context['created_by'] = CustomUserShortSerializer(instance.created_by).data
        return context


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = [
            'id',
            'rate',
            'book',
            'user',
        ]

    def create(self, validated_data):
        book = validated_data['book']
        user = validated_data['user']
        rate = validated_data['rate']
        if book.rating_set.filter(user=user):
            rating = book.rating_set.filter(user=user).last()
            rating.rate = rate
            rating.save()
            return rating
        else:
            return super().create(validated_data)

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['book'] = BookShortSerializer(instance.book).data
        context['user'] = CustomUserShortSerializer(instance.user).data
        return context


class OrderedProductCreateSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.filter(is_active=True))
    count = serializers.IntegerField()

    class Meta:
        model = OrderedProduct
        fields = [
            'book',
            'count',
        ]
    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['price'] = instance.price
        return context

class OrderedProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderedProduct
        fields = [
            'book',
            'count',
            'price'
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['book'] = BookShortSerializer(instance.book).data
        return context


class OrderCreateUpdateSerializer(serializers.ModelSerializer):
    ordered_product = OrderedProductCreateSerializer(many=True, allow_null=False, required=True, write_only=True)
    supplier = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role=User.Role.SUPPLIER), required=False)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'supplier',
            'store',
            'ordered_product',
            'place_of_delivery',
        ]
        extra_kwargs = {
            'customer': {'required': True}
        }

    def create(self, validated_data):
        with transaction.atomic():
            ordered_products = validated_data.pop('ordered_product')
            instance = super().create(validated_data)
            for ordered_product in ordered_products:
                book = ordered_product.get('book')
                count = ordered_product.get('count')
                product = book.product_set.last()
                if product and product.count >= count:
                    discount = Discount.objects.filter(
                        product__book=book,
                        start_date__lte=datetime.datetime.now(),
                        end_date__gte=datetime.datetime.now()
                    ).last()
                    if discount:
                        new_price_with_discount = float(product.price) - (float(product.price) * discount.percent / 100)
                        obj = OrderedProduct.objects.create(book=book, count=count, price=new_price_with_discount)
                    else:
                        obj = OrderedProduct.objects.create(book=book, count=count, price=product.price)
                instance.ordered_product.add(obj)
            return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            ordered_products = validated_data.pop('ordered_product')
            instance.ordered_product.all().delete()
            for ordered_product in ordered_products:
                obj = OrderedProduct.objects.create(**ordered_product)
                instance.ordered_product.add(obj)
            return super().update(instance, validated_data)

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['ordered_product'] = OrderedProductSerializer(instance.ordered_product, many=True).data
        context['store'] = StoreSerializer(instance.store).data
        context['customer'] = CustomUserShortSerializer(instance.customer).data
        return context


class OrderSerializer(serializers.ModelSerializer):
    ordered_product = OrderedProductSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'supplier',
            'store',
            'ordered_product',
            'place_of_delivery',
        ]


class AcceptOrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptOrder
        fields = [
            'id',
            'order'
        ]

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['order'] = OrderSerializer(instance.order).data
        return context

    def create(self, validated_data):
        order = validated_data.get('order')
        products = order.ordered_product.all()
        for product in products:
            obj = Product.objects.filter(store=order.store, book=product.book).last()
            obj.count -= product.count
            obj.save()
        return super().create(validated_data)


class AcceptOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = AcceptOrder
        fields = [
            'id',
            'order'
        ]


class AcceptPaymentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcceptPayment
        fields = [
            'id',
            'order',
            'payment_type',
            'received_amount'
        ]

    def create(self, validated_data):
        order = validated_data.get('order')
        if not order.supplier:
            raise serializers.ValidationError("Личность получателя заказа не указана")
        return super().create(validated_data)

    def to_representation(self, instance):
        context = super().to_representation(instance)
        context['order'] = OrderSerializer(instance.order).data
        return context


class AcceptPaymentSerializer(serializers.ModelSerializer):
    order = OrderSerializer()

    class Meta:
        model = AcceptPayment
        fields = [
            'id',
            'order',
            'payment_type',
            'received_amount'
        ]
