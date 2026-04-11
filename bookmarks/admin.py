from django.contrib import admin
from .models import Bookmark


@admin.register(Bookmark)
class BookmarkAdmin(admin.ModelAdmin):
    list_display  = ('applicant', 'job_title', 'company_name', 'saved_date')
    list_filter   = ('saved_date',)
    search_fields = ('applicant__user__username', 'job_title', 'company_name')
    ordering      = ('-saved_date',)