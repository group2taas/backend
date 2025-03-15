from .services import TestingAgent
from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from loguru import logger
from interviews.models.interview import Interview
from concurrent.futures import ThreadPoolExecutor
import time
import asyncio

BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_TESTING_TOPIC
GROUP_ID = settings.KAFKA_TESTING_GROUP_ID


def process_consumer_message(message_payload):
    interview_id = message_payload.get("interview_id")
    analysis_result = message_payload.get("analysis_result")
    num_test_cases = message_payload.get("num_test_cases")
    logger.info(f"Received analysis result for interview {interview_id}")
    logger.info(f"{interview_id} starting to process now")

    if analysis_result:
        try:
            interview = Interview.objects.get(id=interview_id)
            ticket_id = interview.ticket_id

            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

            testing_agent = TestingAgent(
                ticket_id=ticket_id, num_test_cases=num_test_cases
            )

            loop.run_until_complete(testing_agent.run_tests_async(analysis_result))
            loop.close()
        except Exception as e:
            logger.error(f"Error processing message: {e}")
    else:
        logger.warning("No analysis_result found in message")


def start_testing_consumer():
    consumer_config = {
        "bootstrap.servers": BOOTSTRAP_SERVERS,
        "group.id": GROUP_ID,
        "auto.offset.reset": "earliest",
    }
    consumer = Consumer(consumer_config)
    topic_name = TOPIC_NAME

    consumer.subscribe([topic_name])
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = []
        try:
            while True:
                msg = consumer.poll(1.0)
                if not msg or msg.error():
                    continue

                message_payload = json.loads(msg.value().decode("utf-8"))
                future = executor.submit(process_consumer_message, message_payload)
                futures.append(future)

                futures = [future for future in futures if not future.done()]
        except KeyboardInterrupt:
            logger.error("Consumer interrupted by user")
        finally:
            consumer.close()
