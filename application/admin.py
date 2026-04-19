from django.contrib import admin
from .models import Application, Interview


class InterviewInline(admin.TabularInline):
    model   = Interview
    extra   = 0
    fields  = ('interview_date', 'interview_type', 'interviewer', 'location', 'result')


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display  = ('id', 'applicant', 'job_posting', 'application_date', 'status')
    list_filter   = ('status', 'application_date')
    search_fields = ('applicant__user__fullname', 'job_posting__job_title__title')
    inlines       = [InterviewInline]


@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display  = ('id', 'application', 'interview_date', 'interview_type', 'result')
    list_filter   = ('interview_type', 'result')
    search_fields = ('application__applicant__user__fullname', 'interviewer')