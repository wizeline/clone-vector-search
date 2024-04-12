from os import environ

from dotenv import load_dotenv

load_dotenv()


class Config:
    DEBUG = environ.get("DEBUG")
    LOG_LEVEL = environ.get("LOG_LEVEL")
    S3_BUCKET = environ.get("S3_BUCKET")
    OPENSEARCH_INDEX = environ.get("OPENSEARCH_INDEX")
    OPENSEARCH_CLUSTER_URL = environ.get("OPENSEARCH_CLUSTER_URL")
    IS_LOCAL = environ.get("IS_LOCAL")
    S3_URL = None


class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"
    OPENSEARCH_CLUSTER_URL = "http://host.docker.internal:9200"
    OPENSEARCH_INDEX = "clone-vector-index"
    S3_BUCKET = "clone-ingestion-messages"
    IS_LOCAL = True
    S3_URL = "http://host.docker.internal:4566"
    AWS_ACCESS_KEY_ID = "test"
    AWS_SECRET_ACCESS_KEY = "test"
    AWS_DEFAULT_REGION = "us-east-1"
