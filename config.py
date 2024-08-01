from os import environ

from dotenv import load_dotenv

load_dotenv()


IS_LOCAL = environ.get("IS_LOCAL")


class Config:
    """
    Configuration class
    """

    LOG_LEVEL = environ.get("LOG_LEVEL")
    OPENSEARCH_INDEX = environ.get("OPENSEARCH_INDEX")
    OPENSEARCH_HOST = environ.get("OPENSEARCH_HOST")
    OPENSEARCH_PORT = environ.get("OPENSEARCH_PORT")
    OPENSEARCH_USER = environ.get("OPENSEARCH_USER")
    OPENSEARCH_PASS = environ.get("OPENSEARCH_PASS")
    OPENSEARCH_USE_SSL = environ.get("OPENSEARCH_USE_SSL")
    OPENSEARCH_VERIFY_CERTS = environ.get("OPENSEARCH_VERIFY_CERTS")
    S3_URL = environ.get("S3_URL")


class DevelopmentConfig(Config):
    """
    Development configuration
    """

    LOG_LEVEL = "DEBUG"
    OPENSEARCH_INDEX = "clone-vector-index"
    OPENSEARCH_HOST = "host.docker.internal"
    OPENSEARCH_PORT = "9200"
    OPENSEARCH_USER = ""
    OPENSEARCH_PASS = ""
    OPENSEARCH_USE_SSL = False
    OPENSEARCH_VERIFY_CERTS = False
    S3_URL = "http://host.docker.internal:4566"
