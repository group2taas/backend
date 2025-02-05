from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from .services import AnalysisAgent

BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_ANALYSIS_TOPIC
GROUP_ID = settings.KAFKA_ANALYSIS_GROUP_ID

def start_analysis_consumer():
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
            if msg is None:
                continue
            if msg.error():
                continue

            scoping_data = json.loads(msg.value().decode('utf-8'))

            agent = AnalysisAgent()
            agent.analyze_client_data(scoping_data["scoping_data_id"])
    except KeyboardInterrupt:
        print("Consumer interrupted by user")
    finally:
        consumer.close()
