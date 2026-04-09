from django.db import models

class Application(models.Model):
    # Explicitly defining the ID removes the PyCharm warning
    id = models.BigAutoField(primary_key=True)

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    application_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    remarks = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Application {self.id} - {self.status}"

    class Meta:
        ordering = ['-application_date']