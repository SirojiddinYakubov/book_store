from django.contrib import admin

from common.models import (Category, Store, Rating, ImportProduct, Product, Order, OrderedProduct, Discount)


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active']
    list_display_links = ['title']
    list_filter = ['is_active']
    search_fields = ['title']
    save_on_top = True


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'is_active']
    list_display_links = ['title']
    list_filter = ['is_active']
    search_fields = ['title']
    save_on_top = True


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['id', 'book', 'user', 'rate']
    list_display_links = ['book', 'user', ]
    list_filter = ['is_active', 'created_at']
    search_fields = ['book__title', 'user__email', 'author__last_name', 'author__first_name', 'author__middle_name', ]
    save_on_top = True


@admin.register(ImportProduct)
class ImportProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'book', 'count', 'price']
    list_display_links = ['store']
    list_filter = ['created_at']
    search_fields = ['count']
    save_on_top = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'store', 'book', 'count', 'price', 'created_by']
    list_display_links = ['store']
    list_filter = ['created_at']
    search_fields = ['count']
    save_on_top = True


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'supplier', 'store', 'place_of_delivery']
    list_display_links = ['customer', 'supplier',]
    list_filter = ['created_at']
    search_fields = []
    save_on_top = True


# @admin.register(OrderedProduct)
# class OrderedProductAdmin(admin.ModelAdmin):
#     list_display = ['id', 'book', 'count']
#     list_display_links = ['book']
#     list_filter = ['created_at']
#     search_fields = ['count']
#     save_on_top = True


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'start_date', 'end_date', 'percent', 'created_by']
    list_display_links = ['product']
    list_filter = ['created_at']
    search_fields = []
    save_on_top = True
