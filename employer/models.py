from django.db import models
from accounts.models import User


class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    industry = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'employer_jobcategory'


class JobTitle(models.Model):
    title = models.CharField(max_length=200)
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'employer_jobtitle'


class Employer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='employer_profile'
    )
    company_name = models.CharField(max_length=200)
    company_description = models.TextField(blank=True)
    company_address = models.TextField(blank=True)
    contact_email = models.EmailField(blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    date_registered = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'employer_employer'


class JobPosting(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('closed', 'Closed'),
        ('draft', 'Draft'),
    ]
    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    ]

    employer = models.ForeignKey(
        Employer,
        on_delete=models.CASCADE,
        related_name='job_postings'
    )
    job_title = models.ForeignKey(
        JobTitle,
        on_delete=models.SET_NULL,
        null=True
    )
    category = models.ForeignKey(
        JobCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.TextField()
    requirements = models.TextField()
    location = models.CharField(max_length=200)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='full_time')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    posting_date = models.DateField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.job_title} at {self.employer.company_name}"

    class Meta:
        db_table = 'employer_jobposting'