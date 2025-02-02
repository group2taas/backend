from django.db import models
from tickets.models import Ticket


class Interview(models.Model):
    """
    An Interview object is an OWASP-based security testing interview sheet
    with a collection of questions and answers corresponding to a single ticket.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)

    def __str__(self):
        return f"Response for ticket {self.ticket.id}: {self.ticket}"
