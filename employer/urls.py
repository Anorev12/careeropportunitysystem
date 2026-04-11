from django.urls import path
from . import views

app_name = 'employer'       # ← add this one line

urlpatterns = [
    path('',                 views.employer_index, name='employer_index'),
    path('register/',        views.register_view,  name='register'),
    path('login/',           views.login_view,     name='login'),
    path('logout/',          views.logout_view,    name='logout'),
    path('create/',          views.create_job,     name='create_job'),
    path('edit/<int:id>/',   views.edit_job,       name='edit_job'),
    path('delete/<int:id>/', views.delete_job,     name='delete_job'),
    path('job/<int:id>/',    views.view_job,       name='view_job'),
]