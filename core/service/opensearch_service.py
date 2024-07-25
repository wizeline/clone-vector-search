from logging import Logger

from opensearchpy import OpenSearch

from core.abstracts.services import AbstractOpensearchService


class OpensearchService(AbstractOpensearchService):
    """
    Service class for Opensearch operations.
    """

    def __init__(self, opensearch_client: OpenSearch, index: str, logger: Logger):
        """
        Initialize OpenSearch.

        Args:
            opensearch_client (OpenSearch): Opensearch client
            index (str): the index to query
            logger (Logger): Logger instance.
        """
        self.client = opensearch_client
        self.index = index
        self.logger = logger

    def search(self, query: dict) -> list:
        """
        Performs a query to the configured index

        Args:
            query (dict): the query to perform
        Returns:
            list: a list of dictionaries with the opensearch query document results
        """
        try:
            response = self.client.search(index=self.index, body=query)
            return response["hits"]["hits"]
        except Exception as e:
            error_message = f"Error while searching in OpenSearch: {str(e)}"
            self.logger.error(error_message)
            raise Exception(error_message)
