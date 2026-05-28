from django.contrib import admin
from .models import Interview


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('applicant', 'interview_date', 'interview_type', 'interviewer', 'location', 'result')
    list_filter = ('interview_type', 'result', 'interview_date')
    search_fields = ('applicant', 'interviewer', 'location')
    ordering = ('-interview_date',)