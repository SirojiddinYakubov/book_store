from django.urls import path, include

urlpatterns = [
    path('', include('api.v1.common.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('user/', include('api.v1.user.urls')),
    path('book/', include('api.v1.book.urls')),
]
