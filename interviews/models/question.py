from django.db import models
from django.utils.translation import gettext_lazy as _

from typing import List


class Question(models.Model):
    TEXT = "text"
    SHORT_TEXT = "short-text"
    RADIO = "radio"
    SELECT = "select"
    SELECT_MULTIPLE = "select-multiple"
    INTEGER = "integer"
    FLOAT = "float"
    DATE = "date"
    CHOICES_SEPARATOR = ","

    QUESTION_TYPES = (
        (TEXT, _("text (multiple line)")),
        (SHORT_TEXT, _("short text (one line)")),
        (RADIO, _("radio")),
        (SELECT, _("select")),
        (SELECT_MULTIPLE, _("Select Multiple")),
        (INTEGER, _("integer")),
        (FLOAT, _("float")),
        (DATE, _("date")),
    )

    text = models.TextField()
    is_required = models.BooleanField()
    type = models.CharField(
        _("Type"), max_length=200, choices=QUESTION_TYPES, default=TEXT
    )
    choices = models.TextField(
        _("Choices"),
        blank=True,
        null=True,
        help_text=_(
            """
            Only used if the question type is 'radio', 'select', or 'select multiple'. 
            Provide a comma-separated list of options for this question.
            """
        ),
    )

    def get_choices(self) -> List[str]:
        """Return split and stripped list of choices with no null values."""
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(self.CHOICES_SEPARATOR):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    def __str__(self):
        msg = f"Question '{self.text}' "
        if self.required:
            msg += "(*) "
        msg += f"{self.get_choices()}"
        return msg
