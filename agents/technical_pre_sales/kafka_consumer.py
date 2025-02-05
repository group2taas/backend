from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from .services import TechnicalPreSalesAgent

KAFKA_BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_TECHNICAL_PRE_SALES_TOPIC

def start_technical_pre_sales_consumer():
    consumer_config = {
        'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
        'group.id': settings.KAFKA_GROUP_ID,
        'auto.offset.reset': 'earliest'  
    }
    consumer = Consumer(consumer_config)
    topic_name = settings.KAFKA_TECHNICAL_PRE_SALES_TOPIC

    consumer.subscribe([topic_name])

    try:
        while True:
            msg = consumer.poll(1.0) 
            if msg is None:
                continue
            if msg.error():
                continue

            scoping_data = json.loads(msg.value().decode('utf-8'))

            agent = TechnicalPreSalesAgent()
            agent.analyze_client_data(scoping_data["scoping_data_id"])
    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        consumer.close()
