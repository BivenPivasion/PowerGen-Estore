# <<<<<<< Updated upstream
# from django.contrib import admin
# from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
# from products import views 

# urlpatterns = [
#     path('', views.product_list, name='product_list'),
    
#     path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    
#     path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
    
# ]
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
# =======
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from products import views

urlpatterns = [
    path('products/', views.product_list, name='product_list'),
    path('', views.product_list, name='product_list'),
    path('category/<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# >>>>>>> Stashed changes
