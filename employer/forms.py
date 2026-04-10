from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Employer, JobPosting, JobCategory, JobTitle

User = get_user_model()   # ← gets accounts.User instead of auth.User


class EmployerRegisterForm(UserCreationForm):
    company_name        = forms.CharField(max_length=200)
    company_description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)
    company_address     = forms.CharField(max_length=300, required=False)
    contact_email       = forms.EmailField()
    contact_number      = forms.CharField(max_length=20, required=False)

    class Meta:
        model  = User                              # ← now points to accounts.User
        fields = ['email', 'password1', 'password2']   # ← email not username


class JobPostingForm(forms.Form):
    job_title    = forms.CharField(max_length=200, label="Job Title")
    category     = forms.CharField(max_length=100, label="Category")
    description  = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    requirements = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False)
    location     = forms.CharField(max_length=200)
    salary_min   = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Salary Min")
    salary_max   = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label="Salary Max")
    job_type     = forms.ChoiceField(choices=[
        ('full_time',  'Full Time'),
        ('part_time',  'Part Time'),
        ('contract',   'Contract'),
        ('internship', 'Internship'),
    ])
    status = forms.ChoiceField(choices=[
        ('open',   'Open'),
        ('closed', 'Closed'),
        ('draft',  'Draft'),
    ])
    deadline = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )