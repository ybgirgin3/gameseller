from django.urls import path, include

from product import views

urlpatterns = [
    path('', views.ProductURLPattern, name='home'),
    path('home', views.ProductURLPattern, name='home'),
    path('products/', views.ProductSearch.as_view(), name='product-search'),
    path('categories/', views.CategorySearch.as_view(), name='category-search'),

    # eğer categori detaylarının listelenmemesi ile ilgili olarak bir şey sorulursa
    # categories/<slug> yerine products/<slug:category_slug>/ kullanıldığını bildir
    path('products/<slug:category_slug>/',
         views.CategoryDetail.as_view(), name='category-detail'),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductDetail.as_view(), name='product-detail'),

]
