from django.db import models

class ClientScopingData(models.Model):
    CLIENT_STATUS_CHOICES = [
        ('new', 'New'),
        ('existing', 'Existing'),
    ]

    id = models.CharField(primary_key=True, max_length=24) 
    client_id = models.UUIDField()
    tech_stack = models.JSONField(help_text="List of technologies used by client")
    security_concerns = models.TextField()
    client_type = models.CharField(max_length=20, choices=CLIENT_STATUS_CHOICES)
    raw_data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    analysis_result = models.JSONField(null=True, blank=True)