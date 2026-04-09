from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',       include('accounts.urls')),        # handles / and /login/
    path('',       include('application.urls')),
    path('',       include('employer.urls')),
    path('',       include('bookmarks.urls')),
    path('',       include('notifications.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns = [
    path('',        views.index,       name='index'),   # 127.0.0.1:8080/
    path('login/',  views.login_view,  name='login'),   # 127.0.0.1:8080/login/
    path('logout/', views.logout_view, name='logout'),  # 127.0.0.1:8080/logout/
]