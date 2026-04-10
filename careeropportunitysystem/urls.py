from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/',        admin.site.urls),
    path('accounts/',     include('django.contrib.auth.urls')),
    path('employer/',     include('employer.urls')),
    path('applications/', include('application.urls')),   # ← add this line
    path('',              include('employer.urls')),
]