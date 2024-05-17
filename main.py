import boto3
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from llama_index.vector_stores.opensearch import OpensearchVectorStore, OpensearchVectorClient
from opensearchpy import OpenSearch, RequestsHttpConnection

from config import IS_LOCAL, Config, DevelopmentConfig
from core.controller.vector import VectorController
from core.service.llama_index_service import LlamaIndexService
from core.service.opensearch_service import OpensearchService
from core.service.s3_service import S3Service
from core.usecase.vectorizer import VectorizerUsecase
from core.utils.logger import logger

load_dotenv()

cfg = DevelopmentConfig if IS_LOCAL else Config

app = Flask(__name__)
app.config.from_object(cfg)

opensearch_url = f"{cfg.OPENSEARCH_HOST}:{cfg.OPENSEARCH_PORT}"
if cfg.OPENSEARCH_USE_SSL:
    opensearch_url = f"https://{opensearch_url}"
else:
    opensearch_url = f"http://{opensearch_url}"

# Initialize services and dependencies
# S3 initialization
s3_client = boto3.client('s3', endpoint_url=cfg.S3_URL)
s3_service = S3Service(s3_client, logger)

# Opensearch initialization
opensearch_client = OpenSearch(
    hosts=[{'host': cfg.OPENSEARCH_HOST, 'port': cfg.OPENSEARCH_PORT}],
    http_auth=(cfg.OPENSEARCH_USER, cfg.OPENSEARCH_PASS),
    use_ssl=cfg.OPENSEARCH_USE_SSL,
    verify_certs=cfg.OPENSEARCH_VERIFY_CERTS,
    connection_class=RequestsHttpConnection
)
opensearch_service = OpensearchService(
    opensearch_client,
    cfg.OPENSEARCH_INDEX,
    logger
)

# LlamaIndex initialization
# OpensearchVectorClient stores text in this field by default
text_field = "content"
# OpensearchVectorClient stores embeddings in this field by default
embedding_field = "embedding"
os_vector_client = OpensearchVectorClient(
    opensearch_url, cfg.OPENSEARCH_INDEX, 1536, embedding_field=embedding_field, text_field=text_field
)
vector_store = OpensearchVectorStore(os_vector_client)

llama_service = LlamaIndexService(
    vector_store,
    logger,
)
usecase = VectorizerUsecase(s3_service, llama_service, opensearch_service, logger)
controller = VectorController(usecase, logger)


@app.route("/v1/api/vectorize", methods=["POST"])
def vectorize():
    try:
        request_data = request.get_json()
        return controller.vectoring(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400@app.route("/v1/api/vectorize", methods=["POST"])


@app.route("/v1/api/search", methods=["POST"])
def search():
    try:
        request_data = request.get_json()
        return controller.search(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400


if __name__ == "__main__":
    app.run()
