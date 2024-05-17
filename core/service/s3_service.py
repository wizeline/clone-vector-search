import json
from logging import Logger

from botocore.client import BaseClient

from core.abstracts.services import AbstractS3Service


class S3Service(AbstractS3Service):
    """
    Service class for S3 operations.
    """

    def __init__(self, s3_client: BaseClient, logger: Logger):
        """
        Initialize S3Service.

        Args:
            s3_url (str): URL of the S3 service.
            logger (Logger): Logger instance.
        """
        self.s3_client = s3_client
        self.logger = logger

    def get_object(self, bucket_name: str, object_key: str) -> list:
        """
        Get an object from S3.

        Args:
            bucket_name (str): Name of the S3 bucket.
            object_key (str): Key of the object in the S3 bucket.

        Returns:
            list: List of dictionaries containing the loaded JSON content of the S3 object, or None if an error occurs.
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=object_key)
            json_content = response["Body"].read().decode("utf-8")
            return json.loads(json_content)
        except Exception as e:
            error_message = f"Error while retrieving and loading the S3 file: {str(e)}"
            self.logger.error(error_message)
            raise ValueError(error_message)
