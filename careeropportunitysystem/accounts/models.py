from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# ──────────────────────────────────────────
# User (base authentication table)
# ──────────────────────────────────────────

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('status', 'active')
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('admin', 'Administrator'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    )

    # ERD fields: UserID, Fullname, Email, PhoneNumber, Password, Role, Status
    fullname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fullname', 'role']

    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.fullname} ({self.role})"


# ──────────────────────────────────────────
# Applicant
# ──────────────────────────────────────────

class Applicant(models.Model):
    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('employed', 'Employed'),
        ('not_looking', 'Not Looking'),
    )

    # ERD fields: ApplicantID, Address, DateAssigned, ValidID, AvailabilityStatus
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    address = models.TextField(null=True, blank=True)
    date_assigned = models.DateField(null=True, blank=True)
    valid_id = models.ImageField(upload_to='valid_ids/', null=True, blank=True)
    availability_status = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES, default='available'
    )

    class Meta:
        db_table = 'applicant'

    def __str__(self):
        return f"Applicant: {self.user.fullname}"


# ──────────────────────────────────────────
# Administrator
# ──────────────────────────────────────────

class Administrator(models.Model):
    # ERD fields: AdminID, EmployeeNumber, Department, DateAssigned, PermissionsLevel
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_number = models.CharField(max_length=50, unique=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    date_assigned = models.DateField(null=True, blank=True)
    permissions_level = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'administrator'

    def __str__(self):
        return f"Admin: {self.user.fullname}"


# ──────────────────────────────────────────
# Skill  (linked to Applicant)
# ──────────────────────────────────────────

class Skill(models.Model):
    # ERD fields: SkillID, SkillName, SkillDescription, CategoryType
    applicant = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name='skills'
    )
    skill_name = models.CharField(max_length=100)
    skill_description = models.TextField(null=True, blank=True)
    category_type = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'skill'

    def __str__(self):
        return self.skill_name


# ──────────────────────────────────────────
# Resume  (linked to Applicant)
# ──────────────────────────────────────────

class Resume(models.Model):
    # ERD fields: ResumeID, BackgroundSummary, LastUpdated
    applicant = models.OneToOneField(
        Applicant, on_delete=models.CASCADE, related_name='resume'
    )
    background_summary = models.TextField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resume'

    def __str__(self):
        return f"Resume of {self.applicant.user.fullname}"


# ──────────────────────────────────────────
# Reference  (linked to Applicant via Resume/Applicant)
# ──────────────────────────────────────────

class Reference(models.Model):
    # ERD fields: ReferenceID, ReferenceName, JobTitle, ContactNumber, Email
    applicant = models.ForeignKey(
        Applicant, on_delete=models.CASCADE, related_name='references'
    )
    reference_name = models.CharField(max_length=255)
    job_title = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = 'reference'

    def __str__(self):
        return self.reference_name

