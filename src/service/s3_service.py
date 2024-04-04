import json

import boto3
from abc import ABC, abstractmethod

from botocore.client import BaseClient

from src.utils.logger import logger


class AbstractS3Service(ABC):
    @abstractmethod
    def get_object(self, bucket_name, object_key):
        pass


class S3Service(AbstractS3Service):
    def __init__(self, s3_client: BaseClient):
        self.s3_client = s3_client

    def get_object(self, bucket_name, object_key):
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            json_content = response['Body'].read().decode('utf-8')
            return json.loads(json_content)
        except Exception as e:
            logger.error(f"Error while retrieving and loading the Created S3 file: {str(e)}")
            return None
