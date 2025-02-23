from django.db import models, transaction
from tickets.models import Ticket
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
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
    logs = models.JSONField(default=list)
    progress = models.PositiveIntegerField(default=0)
    pdf = models.FileField(
        upload_to=upload_to,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=["pdf"])],
    )

    def add_log(self, test_log):
        with transaction.atomic():
            result = Result.objects.select_for_update().get(id=self.id)
            result.logs.append(test_log)
            result.progress = len(result.logs)
            result.save(update_fields=["logs", "progress"])

    # def increment_progress(self):
    #     self.progress = models.F("progress") + 1
    #     self.save(update_fields=["progress"])
    #     self.refresh_from_db()

    def __str__(self):
        return self.title
