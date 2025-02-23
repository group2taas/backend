from django.db import models
from users.models import UserProfile


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("new", "Estimating Tests"),
        ("testing", "Testing in Progress"),
        ("error", "Error"),
        ("completed", "Completed"),
    ]
    title = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    details = models.JSONField(default=dict)

    def __str__(self):
        return self.title
