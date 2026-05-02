from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('', views.home_view, name='home_default'),
    path('home/', views.home_view, name='home'),

    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('edit-profile/', views.edit_profile, name='edit_profile'),

    path('records/', views.bookmark_list, name='list'),
    path('add/', views.bookmark_add, name='add'),
    path('<int:pk>/edit/', views.bookmark_edit, name='edit'),
    path('<int:pk>/delete/', views.bookmark_delete, name='delete'),
]