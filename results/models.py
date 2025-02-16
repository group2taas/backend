from django.db import models
from tickets.models import Ticket
from django.core.validators import FileExtensionValidator
import os


def upload_to(instance, filename):
    return os.path.join(
        "results",
        str(instance.user.pk),
        str(instance.ticket.pk),
        str(instance.pk),
        filename,
    )


class Result(models.Model):
    title = models.CharField(max_length=255, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="results")
    progress = models.IntegerField(default=0)
    pdf = models.FileField(
        upload_to=upload_to,
        blank=False,
        null=False,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def increment_progress(self):
        self.progress = models.F("progress") + 1
        self.save(update_fields=["progress"])
        self.refresh_from_db()

    def __str__(self):
        return self.title
