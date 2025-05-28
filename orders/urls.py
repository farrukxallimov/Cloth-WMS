from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list, name='order_list'),
    path('<int:pk>/', views.order_detail, name='order_detail'),
    path('add/', views.order_create, name='order_create'),
    path('customers/', views.customer_list, name='customer_list'),
    path('customers/add/', views.customer_create, name='customer_create'),
    path('deliveries/', views.delivery_list, name='delivery_list'),
    path('<int:pk>/update-delivery/', views.delivery_update, name='delivery_update'),
]
