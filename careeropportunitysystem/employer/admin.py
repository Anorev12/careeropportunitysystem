from django.contrib import admin
from .models import Employer, JobCategory, JobTitle, JobPosting

admin.site.register(Employer)
admin.site.register(JobCategory)
admin.site.register(JobTitle)
admin.site.register(JobPosting)