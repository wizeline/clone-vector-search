from abc import ABC, abstractmethod


# Abstract base class for S3 service
class AbstractS3Service(ABC):
    """
    Abstract class for s3 services.
    """

    @abstractmethod
    def get_object(self, bucket_name, object_key) -> dict:
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
    def vector_store_index(self, twin_id, source_name, file_uuid, documents) -> str:
        """
        Abstract method to indexing documents and store vectors in OpenSearch.

        Args:
            twin_id (str): Identifier for the twin.
            source_name (str): Name of the data source.
            file_uuid (str): UUID of the file containing the documents.
            documents (list): List of dictionaries representing documents.

        Returns:
            str: Index summary
        """
        pass
