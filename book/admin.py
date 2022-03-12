from django.contrib import admin

from book.models import (Book)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'store', 'desc', 'pub_date', 'is_active']
    list_display_links = ['title', 'store']
    list_filter = ['is_active', 'pub_date', ]
    # search_fields = ['author__last_name', 'author__first_name', 'author__middle_name', 'author__email', 'cost', 'title',
    #                  'shop__title']
    save_on_top = True
