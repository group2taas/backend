from elasticsearch import Elasticsearch
import os

class ElasticsearchService:
    def __init__(self):
        self.es = Elasticsearch(
            hosts=[os.getenv("ELASTICSEARCH_URL")]
        )

    def create_index_if_not_exists(self, index_name):
        if not self.es.indices.exists(index=index_name):
            self.es.indices.create(index=index_name)

    def index_document(self, index_name, doc_id, document):
        self.create_index_if_not_exists(index_name)
        return self.es.index(index=index_name, id=doc_id, document=document)

    def search_documents(self, index_name, query):
        return self.es.search(index=index_name, query=query)

    def delete_document(self, index_name, doc_id):
        return self.es.delete(index=index_name, id=doc_id)
