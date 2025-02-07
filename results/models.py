from django.db import models
from tickets.models import Ticket
from django.core.validators import FileExtensionValidator


class Result(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="results")
    pdf = models.FileField(
        upload_to="results/",
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def __str__(self):
        return self.title
