from django.urls import path, include

from product import views

urlpatterns = [
    path('', views.ProductURLPattern, name='home'),
    path('home', views.ProductURLPattern, name='home'),
    path('products/', views.ProductSearch.as_view(), name='product-search'),
    path('categories/', views.CategorySearch.as_view(), name='category-search'),
    path('products/<slug:category_slug>/',
         views.CategoryDetail.as_view(), name='category-detail'),
    path('products/<slug:category_slug>/<slug:product_slug>/',
         views.ProductDetail.as_view(), name='product-detail'),

    # for cart
    # path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    # path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    # path('cart/item_increment/<int:id>/',
    #      views.item_increment, name='item_increment'),
    # path('cart/item_decrement/<int:id>/',
    #      views.item_decrement, name='item_decrement'),
    # path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    # path('cart/cart-detail/', views.cart_detail, name='cart_detail'),
]
