from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import Applicant

User = get_user_model()


class Interview(models.Model):


    INTERVIEW_TYPE_CHOICES = [
        ('initial',   'Initial Interview'),
        ('technical', 'Technical Interview'),
        ('final',     'Final Interview'),
        ('hr',        'HR Interview'),
    ]

    RESULT_CHOICES = [
        ('pending', 'Pending'),
        ('passed',  'Passed'),
        ('failed',  'Failed'),
        ('no_show', 'No Show'),
    ]

    applicant      = models.ForeignKey(Applicant,on_delete=models.CASCADE,related_name='interviews')
    created_by     = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interview_records')

    interview_date = models.DateField()
    interview_type = models.CharField(
        max_length=20,
        choices=INTERVIEW_TYPE_CHOICES,
        default='initial'
    )
    interviewer    = models.CharField(max_length=100)
    location       = models.CharField(max_length=255, blank=True)
    result         = models.CharField(
        max_length=20,
        choices=RESULT_CHOICES,
        default='pending'
    )
    remarks        = models.TextField(blank=True)

    class Meta:
        ordering      = ['-interview_date']
        unique_together = (
            'applicant', 'interview_date', 'interview_type', 'interviewer'
        )

    def __str__(self):
        if self.applicant:
            name = self.applicant.user.get_full_name() or self.applicant.user.username
        else:
            name = "No Applicant"

        return f"{name} — {self.get_interview_type_display()} ({self.interview_date})"