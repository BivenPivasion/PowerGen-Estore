from django.urls import path
from .views import get_liqpay_data, liqpay_callback

urlpatterns = [
   #  path('pay/<int:order_id>/', payment_view, name='payment'),
    path('liqpay/data/<int:order_id>/', get_liqpay_data, name='liqpay-data'),
    path('liqpay/callback/', liqpay_callback, name='liqpay-callback'),
]
