from django.core.management.base import BaseCommand
from agents.testing_agent.kafka_consumer import start_testing_consumer

class Command(BaseCommand):
    def handle(self, *args, **options):
        start_testing_consumer()
