from django.db import models
from django.contrib.auth import get_user_model

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

    created_by     = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='interview_records',
        null=True,
        blank=True
    )
    applicant_name = models.CharField(max_length=255)
    interview_date = models.DateField()
    interview_type = models.CharField(
        max_length=20, choices=INTERVIEW_TYPE_CHOICES, default='initial'
    )
    interviewer    = models.CharField(max_length=100)
    location       = models.CharField(max_length=255, blank=True)
    result         = models.CharField(
        max_length=20, choices=RESULT_CHOICES, default='pending'
    )
    remarks        = models.TextField(blank=True)

    class Meta:
        ordering = ['-interview_date']
        # Prevent duplicate: same applicant, date, type, and interviewer
        unique_together = ('applicant_name', 'interview_date', 'interview_type', 'interviewer')

    def __str__(self):
        return f"{self.applicant_name} — {self.get_interview_type_display()} ({self.interview_date})"