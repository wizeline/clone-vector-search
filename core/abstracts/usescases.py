from abc import ABC, abstractmethod


class AbstractVectorizeUsecase(ABC):
    """
    Abstract class for use vectorize use cases.

    """

    @abstractmethod
    def vectorize_and_index(self, bucket_name, object_key) -> str:
        """
        Abstract method to vectorize and index documents.

        Args:
            bucket_name (str): Name of the S3 bucket containing the document.
            object_key (str): Key of the document object in the S3 bucket.

        Returns:
            str: The indexed document.
        """
        pass
