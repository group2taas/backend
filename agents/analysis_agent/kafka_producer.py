from confluent_kafka import Producer
import json
import os
from django.conf import settings
from loguru import logger

BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_TESTING_TOPIC

producer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_to_testing(scoping_data):
    topic_name = TOPIC_NAME
    producer.produce(
        topic=topic_name,
        value=json.dumps(scoping_data),
        callback=delivery_report
    )
    producer.flush()