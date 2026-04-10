from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


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
        extra_fields.setdefault('role', 'administrator')
        extra_fields.setdefault('status', 'active')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('applicant', 'Applicant'),
        ('employer', 'Employer'),
        ('administrator', 'Administrator'),
    )
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    )
    fullname     = models.CharField(max_length=255)
    email        = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES)
    status       = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    is_staff     = models.BooleanField(default=False)
    is_active    = models.BooleanField(default=True)

    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['fullname', 'role']
    objects = UserManager()

    class Meta:
        db_table = 'user'

    def __str__(self):
        return f"{self.fullname} ({self.get_role_display()})"


class Applicant(models.Model):
    AVAILABILITY_CHOICES = (
        ('available', 'Available'),
        ('employed', 'Currently Employed'),
        ('not_looking', 'Not Looking'),
    )
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='applicant_profile')
    address             = models.TextField(null=True, blank=True)
    date_assigned       = models.DateField(null=True, blank=True)
    valid_id            = models.ImageField(upload_to='valid_ids/', null=True, blank=True)
    availability_status = models.CharField(max_length=20, choices=AVAILABILITY_CHOICES, default='available')

    class Meta:
        db_table = 'applicant'

    def __str__(self):
        return f"Applicant: {self.user.fullname}"


class Administrator(models.Model):
    user              = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_number   = models.CharField(max_length=50, unique=True)
    department        = models.CharField(max_length=100, null=True, blank=True)
    date_assigned     = models.DateField(null=True, blank=True)
    permissions_level = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        db_table = 'administrator'

    def __str__(self):
        return f"Admin: {self.user.fullname}"


class Resume(models.Model):
    applicant          = models.OneToOneField(Applicant, on_delete=models.CASCADE, related_name='resume')
    background_summary = models.TextField(null=True, blank=True)
    last_updated       = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'resume'

    def __str__(self):
        return f"Resume — {self.applicant.user.fullname}"


class Skill(models.Model):
    applicant         = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='skills')
    skill_name        = models.CharField(max_length=100)
    skill_description = models.TextField(null=True, blank=True)
    category_type     = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = 'skill'

    def __str__(self):
        return self.skill_name


class Reference(models.Model):
    applicant      = models.ForeignKey(Applicant, on_delete=models.CASCADE, related_name='references')
    reference_name = models.CharField(max_length=255)
    job_title      = models.CharField(max_length=255, null=True, blank=True)
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    email          = models.EmailField(null=True, blank=True)

    class Meta:
        db_table = 'reference'

    def __str__(self):
        return self.reference_name