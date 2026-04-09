from django.urls import path
from . import views

urlpatterns = [
    path('', views.employer_index, name='employer_index'),
    path('apply/<int:id>/', views.apply_job, name='apply_job'),
    path('edit/<int:id>/', views.edit_job, name='edit_job'),
    path('delete/<int:id>/', views.delete_job, name='delete_job'),
]