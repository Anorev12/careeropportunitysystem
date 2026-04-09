from django.db import models

class Administrator(models.Model):
    AdminID = models.AutoField(primary_key=True)
    EmployeeNumber = models.CharField(max_length=50)
    Department = models.CharField(max_length=100)
    DateAssigned = models.DateField()
    PermissionsLevel = models.IntegerField()

    def __str__(self):
        return self.EmployeeNumber

class Notification(models.Model):
    NotificationID = models.AutoField(primary_key=True)
    MessageContent = models.TextField()
    SentDate = models.DateTimeField()

    def __str__(self):
        return f"Notification {self.NotificationID}"

class AuditLog(models.Model):
    LogID = models.AutoField(primary_key=True)
    ActionTaken = models.CharField(max_length=255)
    EntityAffected = models.CharField(max_length=255)
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log {self.LogID}"