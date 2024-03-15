from abc import ABC, abstractmethod
from opensearchpy import OpenSearch, RequestsHttpConnection


class AbstractOpensearchService(ABC):
    @abstractmethod
    def search(self, query):
        pass


class OpensearchService(AbstractOpensearchService):
    def __init__(self, host, port, username, password, use_ssl, verify_certs, index):
        self.client = OpenSearch(
            hosts=[{'host': host, 'port': port}],
            http_auth=(username, password),
            use_ssl=use_ssl,
            verify_certs=verify_certs,
            connection_class=RequestsHttpConnection
        )
        self.index = index

    def search(self, query):
        try:
            response = self.client.search(index=self.index, body=query)
            return response['hits']['hits']
        except Exception as e:
            # Add robust error handling here
            raise Exception(f"Error searching in OpenSearch: {e}")
