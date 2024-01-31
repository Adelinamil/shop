from django.urls import path

from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.index, name='index'),
    path('where/', views.where, name='where'),
    path('<int:page>/', views.index, name='products_by_page'),
    path('products/<int:page>/<slug:category_slug>/', views.index, name='products_by_category'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
