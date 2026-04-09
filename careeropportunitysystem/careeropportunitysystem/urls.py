from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # gives you login/logout/password reset for free
    path('employer/', include('employer.urls')),
    path('', include('employer.urls')),  # so '/' goes to employer index
]