from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User, Applicant, Administrator


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control', 'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'Password'
        })
    )


class RegisterForm(UserCreationForm):
    first_name   = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name    = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email        = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    role         = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.Select(attrs={'class': 'form-select'}))

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone_number', 'role', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['password1', 'password2']:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserProfileForm(forms.ModelForm):
    class Meta:
        model  = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'status']
        widgets = {
            'first_name':   forms.TextInput(attrs={'class': 'form-control'}),
            'last_name':    forms.TextInput(attrs={'class': 'form-control'}),
            'email':        forms.EmailInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'status':       forms.Select(attrs={'class': 'form-select'}),
        }


class ApplicantProfileForm(forms.ModelForm):
    class Meta:
        model  = Applicant
        fields = ['address', 'valid_id', 'availability_status']
        widgets = {
            'address':             forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'availability_status': forms.Select(attrs={'class': 'form-select'}),
        }