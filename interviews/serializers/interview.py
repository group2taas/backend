from rest_framework import serializers
from interviews.models import Interview, Answer
from .answer import AnswerSerializer

from loguru import logger


class InterviewSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Interview
        fields = ["id", "ticket", "answers", "created_at", "updated_at"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        interview = Interview.objects.create(**validated_data)
        Answer.objects.bulk_create(
            [Answer(interview=interview, **answer_data) for answer_data in answers_data]
        )
        return interview

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", [])
        instance.ticket = validated_data.get("ticket", instance.ticket)
        instance.save()

        # delete old answers and recreate new ones
        instance.answers.all().delete()
        Answer.objects.bulk_create(
            [Answer(interview=instance, **answer_data) for answer_data in answers_data]
        )
        return instance
