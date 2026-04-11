from django.urls import path
from . import views

urlpatterns = [
    path('', views.notifications, name='notifications'),
    path('login/', views.notifications_login, name='notifications_login'),
]