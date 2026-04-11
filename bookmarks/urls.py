from django.urls import path
from . import views

app_name = 'bookmarks'

urlpatterns = [
    path('',             views.bookmark_list,   name='list'),
    path('add/',         views.bookmark_add,    name='add'),
    path('<int:pk>/edit/',   views.bookmark_edit,   name='edit'),
    path('<int:pk>/delete/', views.bookmark_delete, name='delete'),
]