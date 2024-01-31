from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.list_orders, name='list_orders'),
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/pdf/', views.order_pdf, name='order_pdf'),
    path('delete/<int:o_id>/', views.delete_order, name='delete_order'),
]
