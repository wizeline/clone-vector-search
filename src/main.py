import json
from os import environ

import boto3
from dotenv import load_dotenv

from flask import Flask, jsonify
from llama_index.vector_stores.opensearch import OpensearchVectorClient, OpensearchVectorStore

from config import DevelopmentConfig, Config
from controller.controller import Controller
from service.llama_index_service import LlamaIndexService
from service.opensearch_service import OpensearchService
from service.s3_service import S3Service
from usecase.usecase import Usecase
from opensearchpy import OpenSearch, RequestsHttpConnection

load_dotenv()
IS_LOCAL = "IS_LOCAL"

app = Flask(__name__)
is_local = environ.get(IS_LOCAL)
cfg = Config

if is_local:
    cfg = DevelopmentConfig

print(cfg.LOG_LEVEL)
print(cfg.OPENSEARCH_INDEX)
print(cfg.OPENSEARCH_HOST)
print(cfg.OPENSEARCH_PORT)
print(cfg.OPENSEARCH_USER)
print(cfg.OPENSEARCH_PASSWORD)
print(cfg.OPENSEARCH_USE_SSL)
print(cfg.OPENSEARCH_VERIFY_CERTS)
print(cfg.S3_BUCKET)
print(cfg.IS_LOCAL)
print(cfg.S3_URL)
print(cfg.AWS_ACCESS_KEY_ID)
print(cfg.AWS_SECRET_ACCESS_KEY)
print(cfg.AWS_DEFAULT_REGION)

app.config.from_object(cfg)

opensearch_url = f"{cfg.OPENSEARCH_HOST}:{cfg.OPENSEARCH_PORT}"
if cfg.OPENSEARCH_USE_SSL:
    opensearch_url = f"https://{opensearch_url}"
else:
    opensearch_url = f"http://{opensearch_url}"

# Initialize services and dependencies
s3_client = boto3.client('s3', endpoint_url=cfg.S3_URL)
s3_service = S3Service(s3_client)
opensearch_client = OpenSearch(
    hosts=[{'host': cfg.OPENSEARCH_HOST, 'port': cfg.OPENSEARCH_PORT}],
    http_auth=(cfg.OPENSEARCH_USER, cfg.OPENSEARCH_PASSWORD),
    use_ssl=cfg.OPENSEARCH_USE_SSL,
    verify_certs=cfg.OPENSEARCH_VERIFY_CERTS,
    connection_class=RequestsHttpConnection
)

opensearch_service = OpensearchService(
    opensearch_client,
    cfg.OPENSEARCH_INDEX,
)

# OpensearchVectorClient stores text in this field by default
text_field = "content"
# OpensearchVectorClient stores embeddings in this field by default
embedding_field = "embedding"
os_vector_client = OpensearchVectorClient(
    opensearch_url, cfg.OPENSEARCH_INDEX, 1536, embedding_field=embedding_field, text_field=text_field
)
vector_store = OpensearchVectorStore(os_vector_client)

llama_service = LlamaIndexService(vector_store)
usecase = Usecase(s3_service, llama_service, opensearch_service)
controller = Controller(usecase)

# Add the route
app.add_url_rule('/v1/api/vectorize', 'vectorize', controller.vectorize, methods=['POST'])
app.add_url_rule('/v1/api/search', 'search', controller.search, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
