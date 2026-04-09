from django.contrib import admin
from .models import Application


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'job_posting', 'application_date', 'status')
    list_filter = ('status', 'application_date')
    search_fields = ('applicant__address', 'remarks')
    ordering = ('-application_date',)
