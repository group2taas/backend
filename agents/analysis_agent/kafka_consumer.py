from confluent_kafka import Consumer
import json
import os
from django.conf import settings
from .services import AnalysisAgent
from loguru import logger

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

            data = json.loads(msg.value().decode('utf-8'))
            interview_id = data.get("interview_id")
            if interview_id:
                agent = AnalysisAgent()
                agent.analyze_interview(interview_id)
    except KeyboardInterrupt:
        logger.error("Consumer interrupted by user")
    finally:
        consumer.close()
