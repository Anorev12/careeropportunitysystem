from django.contrib import admin
from .models import Administrator, AuditLog, Notification

admin.site.register(Administrator)
admin.site.register(AuditLog)
admin.site.register(Notification)