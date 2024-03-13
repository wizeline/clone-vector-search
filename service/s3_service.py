import boto3
from abc import ABC, abstractmethod


class AbstractS3Service(ABC):
    @abstractmethod
    def get_object(self, bucket_name, object_key):
        pass

    @abstractmethod
    def update_object(self, bucket_name, object_key, data):
        pass


class S3Service(AbstractS3Service):
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def get_object(self, bucket_name, object_key):
        return "Hello from the service layer"
        # try:
        #     response = self.s3_client.get_object(
        #         Bucket=bucket_name,
        #         Key=object_key
        #     )
        #     return response['Body']  # Return the object's content
        # except Exception as e:
        #     # Add robust error handling here
        #     raise Exception(f"Error retrieving object from S3: {e}")

    def update_object(self, bucket_name, object_key, data):
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=object_key,
                Body=data
            )
        except Exception as e:
            # Add robust error handling here
            raise Exception(f"Error updating object in S3: {e}")
