from abc import ABC, abstractmethod
from opensearchpy import OpenSearch


class AbstractOpensearchService(ABC):
    @abstractmethod
    def search(self, query):
        pass


class OpensearchService(AbstractOpensearchService):
    def __init__(self, opensearch_client: OpenSearch, index: str):
        self.client = opensearch_client
        self.index = index

    def search(self, query):
        try:
            response = self.client.search(index=self.index, body=query)
            return response['hits']['hits']
        except Exception as e:
            # Add robust error handling here
            raise Exception(f"Error searching in OpenSearch: {e}")
