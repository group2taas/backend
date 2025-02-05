from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from loguru import logger


BOOTSTRAP_SERVERS = settings.KAFKA_BOOTSTRAP_SERVERS
TOPIC_NAME = settings.KAFKA_TESTING_TOPIC
GROUP_ID = settings.KAFKA_TESTING_GROUP_ID,

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

            assessment_results = json.loads(msg.value().decode('utf-8'))
            logger.info(f"Processing results for {assessment_results['scoping_data_id']}")
            
    except KeyboardInterrupt:
        logger.error("Consumer interrupted by user")
    finally:
        consumer.close()