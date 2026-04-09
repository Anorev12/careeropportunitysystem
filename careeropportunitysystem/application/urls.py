from django.urls import path
from . import views

urlpatterns = [
    path('', views.application_list, name='application_list'),
    path('<int:pk>/', views.application_detail, name='application_detail'),
    path('create/', views.application_create, name='application_create'),
    path('<int:pk>/update/', views.application_update, name='application_update'),
    path('<int:pk>/delete/', views.application_delete, name='application_delete'),
]