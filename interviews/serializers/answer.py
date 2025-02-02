from rest_framework import serializers
from interviews.models import Answer, Question

from loguru import logger


class AnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Answer
        fields = "__all__"

    def _check_answer_for_select(self, choices, body):
        if body:
            answers = body.split(Question.CHOICES_SEPARATOR)
            invalid = set()
            for ans in answers:
                ans = ans.strip()
                if ans and ans not in choices:
                    invalid.add(ans)
            if invalid:
                logger.info(body)
                msg = f"{invalid} not a subset of choices"
                raise serializers.ValidationError(msg)

    def validate(self, data):
        logger.info(f"Validating data for AnswerSerializer: {data}")
        body = data.get("body", "")
        question = data.get("question")
        logger.info(f"Getting question with {question.pk}")
        qtype = question.type

        if qtype == Question.INTEGER and body and body != "":
            try:
                body = int(body)
            except ValueError as e:
                logger.info(body)
                raise serializers.ValidationError("Answer is not an integer")
        if qtype == Question.FLOAT and body and body != "":
            try:
                body = float(body)
            except ValueError as e:
                logger.info(body)
                raise serializers.ValidationError("Answer is not a number")
        if qtype in [Question.RADIO, Question.SELECT, Question.SELECT_MULTIPLE]:
            choices = question.get_choices()
            self._check_answer_for_select(choices, body)

        return data
