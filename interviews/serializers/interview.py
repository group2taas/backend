from rest_framework import serializers
from interviews.models import Interview, Answer
from tickets.models import Ticket
from .answer import AnswerSerializer
from agents.analysis_agent.kafka_producer import send_to_analysis

from loguru import logger


class InterviewSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = Interview
        fields = ["id", "ticket", "created_at", "updated_at", "answers"]

    def validate(self, data):
        """Ensure only one interview for one ticket"""
        if Interview.objects.filter(ticket=data["ticket"].id).exists():
            raise serializers.ValidationError(
                "Only one interview sheet is allowed per ticket."
            )
        return data

    def create(self, validated_data):
        logger.info(f"Receiving data for InterviewSerializer: {validated_data}")
        answers_data = validated_data.pop("answers")
        interview = Interview.objects.create(**validated_data)
        for answer_data in answers_data:
            logger.info(f"Processing answer: {answer_data}")
            Answer.objects.create(interview=interview, **answer_data)
        # Answer.objects.bulk_create(
        #     [Answer(interview=interview, **answer_data) for answer_data in answers_data]
        # )
        send_to_analysis(interview.id)

        return interview

    def update(self, instance, validated_data):
        answers_data = validated_data.pop("answers", [])
        instance.ticket = validated_data.get("ticket", instance.ticket)
        instance.save()

        # delete old answers and recreate new ones
        # TODO: ideally loop through and update / delete answer individually
        # so that `updated_at` and `id` in answer will be reflected correctly
        instance.answers.all().delete()
        Answer.objects.bulk_create(
            [Answer(interview=instance, **answer_data) for answer_data in answers_data]
        )

        return instance
