from django.urls import path
from . import views

app_name = 'interview'

urlpatterns = [
    path('',                 views.index,             name='index'),
    path('login/',           views.interview_login,   name='login'),
    path('register/',        views.interview_register, name='register'),
    path('logout/',          views.interview_logout,  name='logout'),
    path('addNewInterview',  views.add_interview,     name='addNewInterview'),
    path('<int:pk>/edit/',   views.edit_interview,    name='edit'),
    path('<int:pk>/delete/', views.delete_interview,  name='delete'),
]