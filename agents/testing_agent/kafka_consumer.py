from .services import TestingAgent
from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from loguru import logger
from interviews.models.interview import Interview


BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_TESTING_TOPIC
GROUP_ID = settings.KAFKA_TESTING_GROUP_ID

def start_testing_consumer():
    consumer_config = {
        'bootstrap.servers': BOOTSTRAP_SERVERS,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'  
    }
    consumer = Consumer(consumer_config)
    topic_name = TOPIC_NAME

    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(1.0) 
            if not msg or msg.error():
                continue

            message_payload = json.loads(msg.value().decode('utf-8'))
            interview_id = message_payload.get("interview_id")
            analysis_result = message_payload.get("analysis_result")
            logger.info(f"Received analysis result for interview {interview_id}")

            if analysis_result:
                interview = Interview.objects.get(id=interview_id)
                ticket_id = interview.ticket_id
                testing_agent = TestingAgent(ticket_id=ticket_id)
                testing_agent.run_tests(analysis_result)
            else:
                logger.warning("No analysis_result found in message")
    except KeyboardInterrupt:
        logger.error("Consumer interrupted by user")
    finally:
        consumer.close()