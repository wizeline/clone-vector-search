from abc import ABC, abstractmethod
from typing import Any


class AbstractVectorizeUsecase(ABC):
    """
    Abstract class for use vectorize use cases.

    """

    @abstractmethod
    def vectorize_and_index(self, bucket_name: str, object_key: str) -> str:
        """
        Abstract method to vectorize and index documents.

        Args:
            bucket_name (str): Name of the S3 bucket containing the document.
            object_key (str): Key of the document object in the S3 bucket.

        Returns:
            str: The indexed document.
        """
        pass

    @abstractmethod
    def search(self, query: str) -> list[dict[str, Any]]:
        """
        Abstract method to search for indexed documents.

        Args:
            query (str): The text to search documents containing the query text.

        Returns:
            list[dict[str, Any]]: The list of results
        """
        pass
