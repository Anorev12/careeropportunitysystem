from django.urls import path
from . import views

app_name = 'notifications'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.notifications_login, name='login'),
    path('logout/', views.notifications_logout, name='logout'),
    path('list/', views.notifications, name='notifications'),
]