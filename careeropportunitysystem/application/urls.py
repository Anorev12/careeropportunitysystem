from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from accounts.views import index_view  # Make sure this import matches your app name

urlpatterns = [
    path('admin/', admin.site.urls),

    # This fixes the Index page (127.0.0.1:8080/)
    path('', index_view, name='index'),

    # This fixes the Login page (127.0.0.1:8080/login/)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
]