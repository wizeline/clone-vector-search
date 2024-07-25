from abc import ABC, abstractmethod


# Abstract base class for S3 service
class AbstractS3Service(ABC):
    """
    Abstract class for s3 services.
    """

    @abstractmethod
    def get_object(self, bucket_name: str, object_key: str) -> list:
        """
        Abstract method to get an object from S3.

        Args:
            bucket_name (str): Name of the S3 bucket.
            object_key (str): Key of the object in the S3 bucket.

        Returns:
            dict: Dictionary containing the loaded JSON content of the S3 object.
        """
        pass


class AbstractLlamaIndexService(ABC):
    """
    Abstract class for llama index services.
    """

    @abstractmethod
    def vector_store_index(
        self,
        twin_id: str,
        source_name: str,
        channelId: str,
        file_uuid: str,
        documents: list,
    ) -> str:
        """
        Abstract method to indexing documents and store vectors in OpenSearch.

        Args:
            twin_id (str): Identifier for the twin.
            source_name (str): Name of the data source.
            channelId (str): Channel identifier.
            file_uuid (str): UUID of the file containing the documents.
            documents (list): List of dictionaries representing documents.

        Returns:
            str: Index summary
        """
        pass

    @abstractmethod
    def vectorize_string(self, text_input: str) -> list:
        """
        Abstract method to indexing documents and store vectors in OpenSearch.

        Args:
            text_input (str): A string to vectorize

        Returns:
            list: a list of float values representing a vector
        """
        pass


class AbstractOpensearchService(ABC):
    """
    Abstract class for Opensearch services
    """

    @abstractmethod
    def search(self, query: dict) -> list:
        """
        Abstract method to query an opensearch index

        Args:
            query (dict): Opensearch DSL query string

        Returns:
            list: a list of results
        """
        pass
