from django.urls import path
from . import views

urlpatterns = [
    path('list/', views.UserListView.as_view()),
    path('create/', views.UserCreateView.as_view()),
    path('supplier/create/', views.SupplierCreateView.as_view()),
    path('author/create/', views.AuthorCreateView.as_view()),
    path('admin/create/', views.AdminCreateView.as_view()),
    path('update/<int:pk>/', views.UserUpdateView.as_view()),
    path('detail/<int:pk>/', views.UserDetailView.as_view()),
    path('delete/<int:pk>/', views.UserDeleteView.as_view()),

]
