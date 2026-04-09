from django import forms
from .models import JobPosting

class JobPostingForm(forms.ModelForm):
    class Meta:
        model = JobPosting

        fields = [
            'job_title', 'category', 'description', 'requirements',
            'location', 'salary_min', 'salary_max', 'job_type',
            'status', 'deadline'
        ]
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
            'description': forms.Textarea(attrs={'rows': 3}),
            'requirements': forms.Textarea(attrs={'rows': 3}),
        }