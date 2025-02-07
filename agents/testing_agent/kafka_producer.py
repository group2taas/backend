from confluent_kafka import Producer
import json
import os
from django.conf import settings
from loguru import logger

BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
#TBD
TOPIC_NAME = settings.KAFKA_PLACEHOLDER_TOPIC

producer_config = {
    'bootstrap.servers': BOOTSTRAP_SERVERS
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.info(f"Message delivered to {msg.topic()} [{msg.partition()}]")

#TBD
def send_to_placeholder(report):

    topic_name = TOPIC_NAME

    producer.produce(
        topic=topic_name,
        value=json.dumps(report),
        callback=delivery_report
    )
    producer.flush()