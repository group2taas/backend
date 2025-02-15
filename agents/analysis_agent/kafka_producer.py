from confluent_kafka import Producer
import json
import os
from django.conf import settings
from loguru import logger

BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS

producer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_to_testing(analysis_data):
    testing_topic = settings.KAFKA_TESTING_TOPIC
    producer.produce(
        topic=testing_topic,
        value=json.dumps(analysis_data),
        callback=delivery_report
    )
    producer.flush()

def send_to_analysis(interview_id):
    analysis_topic = settings.KAFKA_ANALYSIS_TOPIC
    producer.produce(
        topic=analysis_topic,
        value=json.dumps({"interview_id": interview_id}),
        callback=delivery_report
    )
    producer.flush()