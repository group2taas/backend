from django.db import models

from .question import Question
from .interview import Interview

from loguru import logger


class Answer(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, related_name="answers"
    )
    interview = models.ForeignKey(
        Interview, on_delete=models.CASCADE, related_name="answers"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    body = models.TextField(blank=True, null=True)

    def save(self):
        try:
            _ = Question.objects.get(pk=self.question_id)
        except Question.DoesNotExist:
            logger.warning(
                f"Question {self.question_id} does not exist. Answer will not be saved."
            )
            pass

    def __str__(self):
        return f"Answers to '{self.question}' : '{self.body}'"
