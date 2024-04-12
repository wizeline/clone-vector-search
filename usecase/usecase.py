from abc import ABC, abstractmethod

from service.llama_index_service import AbstractLlamaIndexService
from service.s3_service import AbstractS3Service
from utils.logger import logger


class AbstractUsecase(ABC):
    @abstractmethod
    def vectorize_and_index(self, bucket_name, object_key):
        pass


class Usecase(AbstractUsecase):
    def __init__(
        self,
        s3_service: AbstractS3Service,
        llama_index_service: AbstractLlamaIndexService,
    ):
        self.s3_service = s3_service
        self.llama_index_service = llama_index_service

    def vectorize_and_index(self, bucket_name, object_key):
        json_content = self.s3_service.get_object(bucket_name, object_key)
        if json_content is None:
            logger.info("no documents to index")
            return
        try:
            twin_id, source_name, file_uuid = object_key.split("/")
        except ValueError as e:
            logger.error(
                f"Error while extracting 'twin_id', 'source_name', 'file_uuid' from object key: {str(e)}"
            )
            return
        self.llama_index_service.vector_store_index(
            twin_id, source_name, file_uuid, json_content
        )
        return
