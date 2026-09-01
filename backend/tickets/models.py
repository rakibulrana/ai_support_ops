from django.conf import settings
from django.db import models


class Ticket(models.Model):

    class Status(models.TextChoices):
        NEW = "NEW", "New"
        CLASSIFIED = "CLASSIFIED", "Classified"
        ASSIGNED = "ASSIGNED", "Assigned"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        WAITING_FOR_APPROVAL = "WAITING_FOR_APPROVAL", "Waiting for Approval"
        RESOLVED = "RESOLVED", "Resolved"

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"

    class Category(models.TextChoices):
        BILLING = "BILLING", "Billing"
        TECHNICAL = "TECHNICAL", "Technical"
        ACCOUNT = "ACCOUNT", "Account"
        GENERAL = "GENERAL", "General"

    title = models.CharField(max_length=200)

    description = models.TextField()

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="tickets_created",
    )

    status = models.CharField(
        max_length=30,
        choices=Status.choices,
        default=Status.NEW,
    )

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM,
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.GENERAL,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Ticket {self.id}: {self.title}"

    