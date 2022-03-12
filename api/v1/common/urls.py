from django.urls import path
from . import views

urlpatterns = [
    path('category/list/', views.CategoryListView.as_view()),
    path('category/create/', views.CategoryCreateView.as_view()),
    path('category/detail/<int:pk>/', views.CategoryDetailView.as_view()),
    path('category/update/<int:pk>/', views.CategoryUpdateView.as_view()),
    path('category/delete/<int:pk>/', views.CategoryDeleteView.as_view()),

    path('store/list/', views.StoreListView.as_view()),
    path('store/create/', views.StoreCreateView.as_view()),
    path('store/detail/<int:pk>/', views.StoreDetailView.as_view()),
    path('store/update/<int:pk>/', views.StoreUpdateView.as_view()),
    path('store/delete/<int:pk>/', views.StoreDeleteView.as_view()),

    path('store/<int:store_id>/product/list/', views.StoreProductListView.as_view()),
    path('store/<int:store_id>/product/detail/<int:pk>/', views.StoreProductDetailView.as_view()),
    path('store/<int:store_id>/product/delete/<int:pk>/', views.StoreProductDeleteView.as_view()),

    path('import/product/list/', views.ImportProductListView.as_view()),
    path('import/product/create/', views.ImportProductCreateView.as_view()),
    path('import/product/detail/<int:pk>/', views.ImportProductDetailView.as_view()),

    path('discount/list/', views.DiscountListView.as_view()),
    path('discount/create/', views.DiscountCreateView.as_view()),
    path('discount/detail/<int:pk>/', views.DiscountDetailView.as_view()),
    path('discount/update/<int:pk>/', views.DiscountUpdateView.as_view()),
    path('discount/delete/<int:pk>/', views.DiscountDeleteView.as_view()),

    path('rating/list/', views.RatingListView.as_view()),
    path('rating/create/', views.RatingCreateView.as_view()),

    path('order/list/', views.OrderListView.as_view()),
    path('order/create/', views.OrderCreateView.as_view()),
    path('order/detail/<int:pk>/', views.OrderDetailView.as_view()),
    path('order/update/<int:pk>/', views.OrderUpdateView.as_view()),
    path('order/delete/<int:pk>/', views.OrderDeleteView.as_view()),

    path('accept/order/list/', views.AcceptOrderListView.as_view()),
    path('accept/order/create/', views.AcceptOrderCreateView.as_view()),
    path('accept/order/delete/<int:pk>/', views.AcceptOrderDeleteView.as_view()),

    path('accept/payment/list/', views.AcceptPaymentListView.as_view()),
    path('accept/payment/create/', views.AcceptPaymentCreateView.as_view()),
    path('accept/payment/delete/<int:pk>/', views.AcceptPaymentDeleteView.as_view()),
]
