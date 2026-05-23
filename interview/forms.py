from django import forms
from django.contrib.auth import get_user_model
from .models import Interview

User = get_user_model()


# ── LOGIN ──────────────────────────────────────────────────────────────────
class InterviewLoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username',
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )


# ── REGISTER ───────────────────────────────────────────────────────────────
class InterviewRegisterForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password',
        })
    )
    password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password',
        })
    )

    class Meta:
        model  = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username':   forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First name'}),
            'last_name':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last name'}),
            'email':      forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username is already taken.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('An account with this email already exists.')
        return email

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1')
        p2 = self.cleaned_data.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        if p1 and len(p1) < 8:
            raise forms.ValidationError('Password must be at least 8 characters.')
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


# ── INTERVIEW RECORD ────────────────────────────────────────────────────────
class InterviewForm(forms.ModelForm):

    class Meta:
        model  = Interview
        fields = [
            'applicant_name',
            'interview_date',
            'interview_type',
            'interviewer',
            'location',
            'result',
            'remarks',
        ]
        widgets = {
            'applicant_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Full name of applicant',
            }),
            'interview_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'interview_type': forms.Select(attrs={'class': 'form-control'}),
            'interviewer':    forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Name of interviewer',
            }),
            'location':       forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Room 101 / Online',
            }),
            'result':         forms.Select(attrs={'class': 'form-control'}),
            'remarks':        forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Additional notes...',
            }),
        }

    def clean(self):
        cleaned_data   = super().clean()
        applicant_name = cleaned_data.get('applicant_name')
        interview_date = cleaned_data.get('interview_date')
        interview_type = cleaned_data.get('interview_type')
        interviewer    = cleaned_data.get('interviewer')

        if applicant_name and interview_date and interview_type and interviewer:
            qs = Interview.objects.filter(
                applicant_name=applicant_name,
                interview_date=interview_date,
                interview_type=interview_type,
                interviewer=interviewer,
            )
            # Exclude the current record when editing
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)

            if qs.exists():
                raise forms.ValidationError(
                    f'A {dict(Interview.INTERVIEW_TYPE_CHOICES).get(interview_type)} '
                    f'for "{applicant_name}" with interviewer "{interviewer}" '
                    f'on {interview_date} already exists.'
                )

        return cleaned_data