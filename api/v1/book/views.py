from django.contrib.auth import get_user_model
from django.db.models import F
from rest_framework import generics

from api.v1 import permissions
from book.models import (Book)
from user.tasks import send_report
from . import filters
from . import serializers

User = get_user_model()


class BookListView(generics.ListAPIView):
    """ Список книги """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookSerializer
    filter_class = filters.BookListFilter
    permission_classes = [permissions.AllowAllPermission]


class BookCreateView(generics.CreateAPIView):
    """ Создать книгу """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookCreateUpdateSerializer
    permission_classes = [permissions.AdminPermission]


class BookDetailView(generics.RetrieveAPIView):
    """ О книге подробно """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.AllowAllPermission]


class BookUpdateView(generics.UpdateAPIView):
    """ Редактировать книгу """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.AdminPermission]


class BookDeleteView(generics.DestroyAPIView):
    """ Удалить книгу """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookSerializer
    permission_classes = [permissions.AdminPermission]


class BookRecommendedForUserView(generics.ListAPIView):
    """ Рекомендуется для пользователя """
    queryset = Book.objects.filter(is_active=True)
    serializer_class = serializers.BookSerializer
    permission_classes = [
        permissions.ClientPermission |
        permissions.AdminPermission
    ]

    def get_queryset(self):
        interesting_categories = Book.objects.filter(is_active=True,
                                                     orderedproduct__order__customer_id=self.kwargs.get(
                                                         'user_id')).order_by('-id').annotate(
            value=F('category_id')).values_list('value', flat=True)
        qs = Book.objects.filter(is_active=True, category_id__in=list(set(interesting_categories)))
        return qs

    # def get(self, request, *args, **kwargs):
    #     task = send_report.delay()
    #     print(task.id, task.state, task.status)
    #     return super().get(request, *args, **kwargs)
