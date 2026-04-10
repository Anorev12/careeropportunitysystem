from django import forms
from .models import Bookmark


class BookmarkForm(forms.ModelForm):
    class Meta:
        model  = Bookmark
        fields = ['job_title', 'company_name', 'job_url', 'notes']
        widgets = {
            'job_title':    forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Software Engineer'}),
            'company_name': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Acme Corp'}),
            'job_url':      forms.URLInput(attrs={'class': 'form-input', 'placeholder': 'https://...'}),
            'notes':        forms.Textarea(attrs={'class': 'form-input', 'rows': 3, 'placeholder': 'Any notes about this job...'}),
        }