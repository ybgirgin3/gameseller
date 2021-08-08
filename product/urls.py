from django.urls import path, include

from product import views

urlpatterns = [
    path('', views.ProductURLPattern, name='home'),
    path('home', views.ProductURLPattern, name='home'),
    path('products/', views.ProductSearch.as_view(), name='product-search'),
    path('categories/', views.CategorySearch.as_view(), name='category-search'),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view(), name='product-detail'),
    
]
