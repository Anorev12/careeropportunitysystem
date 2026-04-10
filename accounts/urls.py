from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('',           views.index,        name='index'),
    path('login/',     views.login_view,   name='login'),
    path('logout/',    views.logout_view,  name='logout'),
    path('register/',  views.register_view, name='register'),
    path('dashboard/', views.dashboard,    name='dashboard'),
    path('profile/',   views.profile_view, name='profile'),
    path('users/',     views.user_list,    name='user_list'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
]