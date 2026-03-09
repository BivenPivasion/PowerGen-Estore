
from django.urls import path
from django.contrib.auth import views as auth_views
from card import views

urlpatterns = [
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/minus/<int:product_id>/', views.cart_minus, name='cart_minus'),
    path('cart/add_with_quantity/<int:product_id>/', views.cart_add_with_quantity, name='cart_add_with_quantity'),
    path('cart/remove/', views.card_remove, name='card_remove'),
    path('cart/remove/<int:product_id>/', views.cart_remove_product, name='cart_remove_product'),
    # path('checkout/', views.checkout, name='checkout'),
    # path('payment/<int:order_id>/', views.payment, name='payment'),
    # path('card_add_product_detail/', views.card_add_product_detail, name='card_add_product_detail')
]
