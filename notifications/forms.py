from django import forms
from .models import Notification

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['message_content']
        widgets = {
            'message_content': forms.Textarea(attrs={
                'style': 'width:100%;padding:10px 14px;border:1.5px solid #ddd;border-radius:8px;font-size:14px;box-sizing:border-box;',
                'placeholder': 'Enter message content',
                'rows': 4
            }),
        }