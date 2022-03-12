from django.contrib.auth import get_user_model
from rest_framework import serializers
from book.models import Book

User = get_user_model()


class BookCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'category',
            'store',
            'image',
            'desc',
            'author',
            'pub_date',
        ]

    def validate(self, attrs):
        errors = dict()

        if attrs.get('author', None):
            for author in attrs['author']:
                if author.role != User.Role.AUTHOR:
                    errors.update(author=["Это поле принимает только роль писателя."])

        if errors.__len__() > 0:
            raise serializers.ValidationError(errors)
        return attrs

    def to_representation(self, instance):
        from api.v1.common.serializers import CategorySerializer, StoreSerializer
        from api.v1.user.serializers import CustomUserShortSerializer
        context = super().to_representation(instance)
        context['store'] = StoreSerializer(instance.store).data
        context['category'] = CategorySerializer(instance.category).data
        context['author'] = CustomUserShortSerializer(instance.author, many=True).data
        return context

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
            'category',
            'store',
            'image',
            'desc',
            'author',
            'pub_date',
        ]

    def to_representation(self, instance):
        from api.v1.common.serializers import CategorySerializer, StoreSerializer
        from api.v1.user.serializers import CustomUserShortSerializer
        context = super().to_representation(instance)
        context['store'] = StoreSerializer(instance.store).data
        context['category'] = CategorySerializer(instance.category).data
        context['author'] = CustomUserShortSerializer(instance.author, many=True).data
        return context

class BookShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'id',
            'title',
        ]