from django.db import models
from accounts.models import Applicant


class Bookmark(models.Model):
    """
    ERD: Bookmark — BookmarkID, SavedDate, Notes
    Links an Applicant to a job posting they saved.
    Uses a generic job_title + company_name so it works independently
    of whether the employer app's JobPosting model exists yet.
    """
    applicant    = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name='bookmarks'
    )
    job_title    = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255, blank=True)
    job_url      = models.URLField(blank=True, help_text="Link to the job posting")
    saved_date   = models.DateField(auto_now_add=True)
    notes        = models.TextField(blank=True)

    class Meta:
        ordering = ['-saved_date']

    def __str__(self):
        return f"{self.applicant.user.username} → {self.job_title}"