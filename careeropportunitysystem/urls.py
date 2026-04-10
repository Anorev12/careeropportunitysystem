from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

# Root URL (127.0.0.1:8080/) redirects to the accounts index page
urlpatterns = [
    path('admin/',         admin.site.urls),
    path('',               lambda req: redirect('accounts:index'), name='home'),
    path('accounts/',      include('accounts.urls',      namespace='accounts')),
    path('employer/',      include('employer.urls')),
    path('bookmarks/',     include('bookmarks.urls')),
    path('notifications/', include('notifications.urls')),
    path('application/',   include('application.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)