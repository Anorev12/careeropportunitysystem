from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['applicant', 'job_posting', 'status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4}),
            'status': forms.Select(),
        }