from abc import ABC, abstractmethod
from service.s3_service import AbstractS3Service


class AbstractUsecase(ABC):
    @abstractmethod
    def get_object(self, bucket_name, object_key):
        pass


class Usecase(AbstractUsecase):
    def __init__(self, s3_service: AbstractS3Service):
        self.s3_service = s3_service

    def get_object(self, bucket_name, object_key):
        return self.s3_service.get_object(bucket_name, object_key)