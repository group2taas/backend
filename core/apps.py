from django.apps import AppConfig
import threading
from core.logging import logger
from django.db.models.signals import post_migrate
from services.sync_mongodb_to_es import SyncMongoToElasticsearch


class CoreConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

    def ready(self):
        self.stop_event = threading.Event() 
        post_migrate.connect(self.run_sync_service, sender=self)
        self.sync_thread = None

    def run_sync_service(self, **kwargs):
        index_name = "index_name"  # Replace
        sync_service = SyncMongoToElasticsearch(index_name=index_name)

        def start_sync():
            logger.info("Starting initial sync to Elasticsearch.")
            try:
                while not self.stop_event.is_set():  
                    sync_service.sync_all_documents()  # Initial
                    # sync_service.start_change_stream()  # RealTime
                    break
            except Exception as e:
                logger.error(f"Error during sync service: {e}")
        
        if self.sync_thread is None or not self.sync_thread.is_alive():
            self.sync_thread = threading.Thread(target=start_sync, daemon=True, name="SyncThread")
            self.sync_thread.start()

    def shutdown_sync_service(self):
        if self.sync_thread and self.sync_thread.is_alive():
            self.stop_event.set()
            self.sync_thread.join(timeout=10) 

    def __del__(self):
        self.shutdown_sync_service()