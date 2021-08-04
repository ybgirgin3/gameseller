from django.urls import path, include

from product import views

urlpatterns = [
    #path("", views.HomeView.as_view(), name='home'),
    #path("home/", views.HomeView.as_view(), name='home'),
    #path('latest-products/', views.LatestProductsList.as_view(), name='lastest'),
    path('', views.LatestProductsList.as_view(), name='home'),
    path('home', views.LatestProductsList.as_view(), name='home'),
    path('products/', views.ProductSearch.as_view(), name='product-search'),
    path('categories/', views.CategorySearch.as_view(), name='category-search'),
    path('products/<slug:category_slug>/', views.CategoryDetail.as_view(), name='category-detail'),
    path('products/<slug:category_slug>/<slug:product_slug>/', views.ProductDetail.as_view(), name='product-detail'),
    
]
