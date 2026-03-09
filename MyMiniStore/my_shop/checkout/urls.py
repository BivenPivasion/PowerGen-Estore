from django.urls import path
from checkout import views

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:order_id>/', views.order_success, name='order_success'),
]