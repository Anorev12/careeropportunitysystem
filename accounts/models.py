from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom User model — ERD User entity.
    AbstractUser provides: id, username, first_name, last_name,
    email, password, is_active, date_joined, last_login.
    """
    ROLE_CHOICES = [
        ('applicant', 'Applicant'),
        ('employer',  'Employer'),
        ('admin',     'Administrator'),
    ]
    STATUS_CHOICES = [
        ('active',    'Active'),
        ('inactive',  'Inactive'),
        ('suspended', 'Suspended'),
    ]

    phone_number = models.CharField(max_length=20, blank=True)
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES, default='applicant')
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    @property
    def fullname(self):
        return self.get_full_name() or self.username

    def __str__(self):
        return f"{self.username} — {self.get_role_display()}"


class Applicant(models.Model):
    """ERD Applicant entity: ApplicantID, Address, DateAssigned, ValidID, AvailabilityStatus"""
    AVAILABILITY_CHOICES = [
        ('available',     'Available'),
        ('not_available', 'Not Available'),
        ('employed',      'Currently Employed'),
    ]
    user                = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='applicant_profile',
        limit_choices_to={'role': 'applicant'}
    )
    address             = models.TextField(blank=True)
    date_assigned       = models.DateField(auto_now_add=True)
    valid_id            = models.ImageField(upload_to='valid_ids/', null=True, blank=True)
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='available'
    )

    def __str__(self):
        return f"Applicant: {self.user.fullname}"


class Administrator(models.Model):
    """ERD Administrator entity: AdminID, EmployeeNumber, Department, DateAssigned, PermissionsLevel"""
    PERMISSION_CHOICES = [
        ('1', 'Level 1 – View Only'),
        ('2', 'Level 2 – Edit'),
        ('3', 'Level 3 – Full Access'),
    ]
    user              = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='admin_profile',
        limit_choices_to={'role': 'admin'}
    )
    employee_number   = models.CharField(max_length=50, unique=True)
    department        = models.CharField(max_length=100, blank=True)
    date_assigned     = models.DateField(auto_now_add=True)
    permissions_level = models.CharField(
        max_length=1, choices=PERMISSION_CHOICES, default='1'
    )

    def __str__(self):
        return f"Admin: {self.user.fullname} (Level {self.permissions_level})"