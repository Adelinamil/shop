from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('check_user/', views.check_user, name='check_user'),
    path('confirm_password/', views.confirm_password, name='confirm_password'),
]
