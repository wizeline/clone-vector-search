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


class DevelopmentConfig(Config):
    LOG_LEVEL = "DEBUG"
    OPENSEARCH_CLUSTER_URL = "http://localhost:9200"
    OPENSEARCH_INDEX = "clone-vector-index"
    IS_LOCAL = True
