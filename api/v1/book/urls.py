from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.BookListView.as_view()),
    path('create/', views.BookCreateView.as_view()),
    path('detail/<int:pk>/', views.BookDetailView.as_view()),
    path('update/<int:pk>/', views.BookUpdateView.as_view()),
    path('delete/<int:pk>/', views.BookDeleteView.as_view()),

    path('recommended-for-user/<int:user_id>/', views.BookRecommendedForUserView.as_view()),
]
