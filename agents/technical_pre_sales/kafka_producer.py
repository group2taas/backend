from confluent_kafka import Producer
import json
import os
from django.conf import settings

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS

producer_config = {
    'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS
}
producer = Producer(producer_config)

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def send_to_sales(scoping_data):
    topic_name = settings.KAFKA_TECHNICAL_PRE_SALES_TOPIC
    producer.produce(
        topic=topic_name,
        value=json.dumps(scoping_data),
        callback=delivery_report
    )
    producer.flush()