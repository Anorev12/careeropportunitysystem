from django.db import models
from accounts.models import User


class Notification(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='notifications'
    )
    message_content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user.username} - {self.sent_date}"

    class Meta:
        ordering = ['-sent_date']


class AuditLog(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action_taken = models.CharField(max_length=255)
    entity_affected = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action_taken} on {self.entity_affected} at {self.timestamp}"

    class Meta:
        ordering = ['-timestamp']