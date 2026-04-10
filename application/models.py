from django.db import models
from accounts.models import Applicant
from employer.models import JobPosting


# ──────────────────────────────────────────
# Application
# ──────────────────────────────────────────

class Application(models.Model):
    STATUS_CHOICES = (
        ('pending',   'Pending'),
        ('reviewed',  'Reviewed'),
        ('accepted',  'Accepted'),
        ('rejected',  'Rejected'),
        ('withdrawn', 'Withdrawn'),
    )

    # ERD fields: ApplicationID, ApplicationDate, Status, Remarks
    applicant        = models.ForeignKey(Applicant,  on_delete=models.CASCADE, related_name='applications')
    job_posting      = models.ForeignKey(JobPosting, on_delete=models.CASCADE, related_name='applications')
    application_date = models.DateField(auto_now_add=True)
    status           = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks          = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'application'
        unique_together = ('applicant', 'job_posting')

    def __str__(self):
        return f"{self.applicant.user.fullname} -> {self.job_posting} [{self.status}]"


# ──────────────────────────────────────────
# Interview
# ──────────────────────────────────────────

class Interview(models.Model):
    TYPE_CHOICES = (
        ('phone',     'Phone'),
        ('video',     'Video'),
        ('in_person', 'In-Person'),
        ('technical', 'Technical'),
    )

    RESULT_CHOICES = (
        ('passed',  'Passed'),
        ('failed',  'Failed'),
        ('pending', 'Pending'),
        ('no_show', 'No Show'),
    )

    # ERD fields: InterviewID, InterviewDate, InterviewType, Interviewer, Location, Result, Remarks
    application    = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='interviews')
    interview_date = models.DateTimeField()
    interview_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='in_person')
    interviewer    = models.CharField(max_length=255, null=True, blank=True)
    location       = models.CharField(max_length=255, null=True, blank=True)
    result         = models.CharField(max_length=20, choices=RESULT_CHOICES, default='pending')
    remarks        = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'interview'

    def __str__(self):
        return f"Interview for {self.application} on {self.interview_date}"