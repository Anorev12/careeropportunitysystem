from django import forms
from .models import Application, Interview


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['job_posting', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Optional cover note or message...'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    """Used by employer/admin to update status & add remarks."""
    class Meta:
        model = Application
        fields = ['status', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }


class InterviewForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['interview_date', 'interview_type', 'interviewer', 'location', 'result', 'remarks']
        widgets = {
            'interview_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'remarks': forms.Textarea(attrs={'rows': 3}),
        }