from rest_framework import serializers
from interviews.models import Question
from loguru import logger


class QuestionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = "__all__"

    def validate(self, data):
        """Verifies that there is at least two choices

        Args:
            choices (str):  The string representing the user choices.
        """
        qtype = data.get("type", "")
        choices = data.get("choices", "")
        if qtype in [Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE]:
            values = choices.split(Question.CHOICES_SEPARATOR)
            if len(values) < 2:
                logger.info(values)
                msg = "The selected field requires an associated list of choices of more than one item."
                raise serializers.ValidationError(msg)

        return data
