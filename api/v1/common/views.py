from rest_framework import generics, status
from rest_framework.response import Response

from api.v1 import permissions
from common.models import (Category, Store, Product, ImportProduct, Discount, Rating, Order, AcceptOrder, AcceptPayment)
from . import serializers


class CategoryListView(generics.ListAPIView):
    """ Список категорий """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AllowAllPermission]


class CategoryCreateView(generics.CreateAPIView):
    """ Создать категорию """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AdminPermission]


class CategoryDetailView(generics.RetrieveAPIView):
    """ О категории подробно """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AllowAllPermission]


class CategoryUpdateView(generics.UpdateAPIView):
    """ Редактировать категорию """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AdminPermission]


class CategoryDeleteView(generics.DestroyAPIView):
    """ Удалить категорию """
    queryset = Category.objects.filter(is_active=True)
    serializer_class = serializers.CategorySerializer
    permission_classes = [permissions.AdminPermission]


class StoreListView(generics.ListAPIView):
    """ Список магазинов """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.AllowAllPermission]


class StoreCreateView(generics.CreateAPIView):
    """ Создать магазин """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.AdminPermission]


class StoreDetailView(generics.RetrieveAPIView):
    """ О магазине подробно """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.AllowAllPermission]


class StoreUpdateView(generics.UpdateAPIView):
    """ Редактировать магазин """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.AdminPermission]


class StoreDeleteView(generics.DestroyAPIView):
    """ Удалить магазин """
    queryset = Store.objects.filter(is_active=True)
    serializer_class = serializers.StoreSerializer
    permission_classes = [permissions.AdminPermission]


class StoreProductListView(generics.ListAPIView):
    """ Список товаров на складе """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAllPermission]

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        qs = super().get_queryset().filter(store_id=store_id)
        return qs

class StoreProductDetailView(generics.RetrieveAPIView):
    """ O товарах на складе """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AllowAllPermission]

    def get_object(self):
        obj = super().get_object()
        store_id = self.kwargs.get('store_id')
        qs = Product.objects.filter(store_id=store_id).values_list('id', flat=True)
        if self.kwargs.get('pk') in list(qs):
            return obj

class StoreProductDeleteView(generics.DestroyAPIView):
    """ Удаление товара на складе """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.AdminPermission]

    def get_queryset(self):
        store_id = self.kwargs.get('store_id')
        qs = super().get_queryset().filter(store_id=store_id)
        return qs

class ImportProductListView(generics.ListAPIView):
    """ Список добавленных товаров на складе """
    queryset = ImportProduct.objects.filter(is_active=True)
    serializer_class = serializers.ImportProductSerializer
    permission_classes = [permissions.AdminPermission]


class ImportProductCreateView(generics.CreateAPIView):
    """ добавленных товаров на склад """
    queryset = ImportProduct.objects.filter(is_active=True)
    serializer_class = serializers.ImportProductCreateSerializer
    permission_classes = [permissions.AdminPermission]


class ImportProductDetailView(generics.RetrieveAPIView):
    """ O добавленных товаров на склад """
    queryset = ImportProduct.objects.filter(is_active=True)
    serializer_class = serializers.ImportProductSerializer
    permission_classes = [permissions.AdminPermission]


class DiscountListView(generics.ListAPIView):
    """ Список скидков """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.AdminPermission]


class DiscountCreateView(generics.CreateAPIView):
    """ Создать скидку """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.AdminPermission]


class DiscountDetailView(generics.RetrieveAPIView):
    """ О скидке подробно """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.AdminPermission]


class DiscountUpdateView(generics.UpdateAPIView):
    """ Редактировать скидку """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.AdminPermission]


class DiscountDeleteView(generics.DestroyAPIView):
    """ Удалить скидку """
    queryset = Discount.objects.filter(is_active=True)
    serializer_class = serializers.DiscountSerializer
    permission_classes = [permissions.AdminPermission]



class RatingListView(generics.ListAPIView):
    """ Список оценок """
    queryset = Rating.objects.filter(is_active=True)
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.AdminPermission]


class RatingCreateView(generics.CreateAPIView):
    """ Создать оценку """
    queryset = Rating.objects.filter(is_active=True)
    serializer_class = serializers.RatingSerializer
    permission_classes = [permissions.AllowAllPermission]




class OrderListView(generics.ListAPIView):
    """ Список заказов """
    queryset = Order.objects.filter(is_active=True)
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AdminPermission]


class OrderCreateView(generics.CreateAPIView):
    """ Создать заказ """
    queryset = Order.objects.filter(is_active=True)
    serializer_class = serializers.OrderCreateUpdateSerializer
    permission_classes = [permissions.AllowAllPermission]


class OrderDetailView(generics.RetrieveAPIView):
    """ О заказе подробно """
    queryset = Order.objects.filter(is_active=True)
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AllowAllPermission]


class OrderUpdateView(generics.UpdateAPIView):
    """ Редактировать заказ """
    queryset = Order.objects.filter(is_active=True)
    serializer_class = serializers.OrderCreateUpdateSerializer
    permission_classes = [permissions.AllowAllPermission]


class OrderDeleteView(generics.DestroyAPIView):
    """ Удалить заказ """
    queryset = Order.objects.filter(is_active=True)
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.AllowAllPermission]



class AcceptOrderListView(generics.ListAPIView):
    """ Список принятый заказы """
    queryset = AcceptOrder.objects.filter(is_active=True)
    serializer_class = serializers.AcceptOrderSerializer
    permission_classes = [
        permissions.AdminPermission |
        permissions.SupplierPermission
    ]


class AcceptOrderCreateView(generics.CreateAPIView):
    """ Принять заказ """
    queryset = AcceptOrder.objects.filter(is_active=True)
    serializer_class = serializers.AcceptOrderCreateSerializer
    permission_classes = [
        permissions.AdminPermission
    ]


class AcceptOrderDeleteView(generics.DestroyAPIView):
    """ Удалить принятый заказ """
    queryset = AcceptOrder.objects.filter(is_active=True)
    serializer_class = serializers.AcceptOrderSerializer
    permission_classes = [
        permissions.AdminPermission
    ]




class AcceptPaymentListView(generics.ListAPIView):
    """ Cписок принятых платежей """
    queryset = AcceptPayment.objects.filter(is_active=True)
    serializer_class = serializers.AcceptPaymentSerializer
    permission_classes = [
        permissions.AdminPermission |
        permissions.SupplierPermission
    ]


class AcceptPaymentCreateView(generics.CreateAPIView):
    """ Принимать платеж """
    queryset = AcceptPayment.objects.filter(is_active=True)
    serializer_class = serializers.AcceptPaymentCreateSerializer
    permission_classes = [
        permissions.AdminPermission |
        permissions.SupplierPermission
    ]


class AcceptPaymentDeleteView(generics.DestroyAPIView):
    """ Удалить платеж """
    queryset = AcceptPayment.objects.filter(is_active=True)
    serializer_class = serializers.AcceptPaymentSerializer
    permission_classes = [
        permissions.AdminPermission |
        permissions.SupplierPermission
    ]