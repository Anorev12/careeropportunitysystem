from django.urls import path
from . import views

urlpatterns = [
    path('',                 views.employer_index, name='employer_index'),
    path('create/',          views.create_job,     name='create_job'),
    path('edit/<int:id>/',   views.edit_job,       name='edit_job'),
    path('delete/<int:id>/', views.delete_job,     name='delete_job'),
    path('job/<int:id>/',    views.view_job,       name='view_job'),
]