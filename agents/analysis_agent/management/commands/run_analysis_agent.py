from django.core.management.base import BaseCommand
from agents.analysis_agent.kafka_consumer import start_analysis_consumer

class Command(BaseCommand):
    def handle(self, *args, **options):
        start_analysis_consumer()
