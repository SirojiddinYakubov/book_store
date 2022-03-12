import operator
from functools import reduce

import django_filters as filters
from django.db.models import Q

from book.models import Book


class BookListFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr="icontains")
    category = filters.CharFilter(field_name="category__title", lookup_expr="icontains")
    author = filters.CharFilter(
            method='author_filter'
        )

    def author_filter(self, queryset, name, value):
        values = value.split(' ')
        qs = queryset.filter(reduce(operator.and_, (
            Q(author__first_name__icontains=value) | Q(author__last_name__icontains=value) | Q(
                author__middle_name__icontains=value) for value in values)))
        return qs

    class Meta:
        model = Book
        fields = {
            'title',
            'author',
            'category',
        }