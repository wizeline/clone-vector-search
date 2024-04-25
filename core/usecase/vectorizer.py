from logging import Logger

from core.abstracts.usescases import AbstractVectorizeUsecase
from core.service.llama_index_service import AbstractLlamaIndexService
from core.service.s3_service import AbstractS3Service


class VectorizerUsecase(AbstractVectorizeUsecase):
    def __init__(
        self,
        s3_service: AbstractS3Service,
        llama_index_service: AbstractLlamaIndexService,
        logger: Logger,
    ):
        """
        Initialize the Usecase.

        Args:
            s3_service (AbstractS3Service): An instance of a class implementing the AbstractS3Service interface.
            llama_index_service (AbstractLlamaIndexService): An instance of a class implementing the AbstractLlamaIndexService interface.
        """
        self.s3_service = s3_service
        self.llama_index_service = llama_index_service
        self.logger = logger

    def vectorize_and_index(self, bucket_name, object_key) -> str:
        """
        This method retrieves JSON content from the specified S3 bucket and delegates indexing tasks
        to the llama_index_service.

        Args:
            bucket_name (str): Name of the S3 bucket containing the document.
            object_key (str): Key of the document object in the S3 bucket.

        Returns:
            str: The indexed document.
        """

        json_content = self.s3_service.get_object(bucket_name, object_key)
        self.logger.info(f"Received vectorization request for {object_key}")
        if json_content is None:
            error_message = "Not content to be indexing"
            self.logger.error(error_message)
            raise ValueError(error_message)
        try:
            twin_id, source_name, file_uuid = object_key.split("/")
            return self.llama_index_service.vector_store_index(
                twin_id, source_name, file_uuid, json_content
            )
        except ValueError as e:
            self.logger.error(e)
            raise ValueError(e)
