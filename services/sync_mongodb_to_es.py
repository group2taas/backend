from core.services import elasticsearch_service
from django.apps import apps
from users.models import UserProfile
import os


class SyncMongoToElasticsearch:
    def __init__(self, index_name):
        self.index_name = index_name

    def sync_all_documents(self):

        for document in UserProfile.objects.all():  # Replace 
            doc_id = str(document.uid) 
            document_data = document.to_dict() 
            elasticsearch_service.index_document(self.index_name, doc_id, document_data)

    def start_change_stream(self):

        with self.collection.watch() as stream:
            for change in stream:
                operation_type = change["operationType"]
                doc_id = str(change["documentKey"]["_id"])

                if operation_type in ["insert", "update"]:
                    full_document = change.get("fullDocument", {})
                    elasticsearch_service.index_document(self.index_name, doc_id, full_document)

                elif operation_type == "delete":
                    elasticsearch_service.delete_document(self.index_name, doc_id)
