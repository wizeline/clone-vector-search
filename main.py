import boto3
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from llama_index.vector_stores.opensearch import (
    OpensearchVectorClient,
    OpensearchVectorStore,
)
from opensearchpy import OpenSearch, RequestsHttpConnection

from config import Config
from core.controller.vector import VectorController
from core.service.llama_index_service import LlamaIndexService
from core.service.opensearch_service import OpensearchService
from core.service.s3_service import S3Service
from core.usecase.vectorizer import VectorizerUsecase
from core.utils.definitions import MAPPINGS
from core.utils.logger import logger

load_dotenv()

app = Flask(__name__)
cfg = Config()

app.config.from_object(cfg)
s3_client = boto3.client("s3")
s3_service = S3Service(s3_client, logger)
host = {"host": cfg.OPENSEARCH_HOST, "port": cfg.OPENSEARCH_PORT}

# Opensearch initialization
try:
    opensearch_client = OpenSearch(
        hosts=[host],
        http_auth=(cfg.OPENSEARCH_USER, cfg.OPENSEARCH_PASS),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
    )
    if not opensearch_client.indices.exists(index=cfg.OPENSEARCH_INDEX):
        opensearch_client.indices.create(index=cfg.OPENSEARCH_INDEX, body=MAPPINGS)
except Exception as e:
    logger.error(f"Failed to connect to OpenSearch: {e}")
    raise


opensearch_service = OpensearchService(opensearch_client, cfg.OPENSEARCH_INDEX, logger)

text_field = "content"
embedding_field = "embedding"
try:
    os_vector_client = OpensearchVectorClient(
        cfg.OPENSEARCH_HOST,
        cfg.OPENSEARCH_INDEX,
        1536,
        embedding_field=embedding_field,
        text_field=text_field,
        http_auth=(cfg.OPENSEARCH_USER, cfg.OPENSEARCH_PASS),
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection,
        timeout=10,
        port="",
    )
    vector_store = OpensearchVectorStore(os_vector_client)
except Exception as e:
    logger.error(f"Failed to initialize OpensearchVectorClient: {e}")
    raise

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
        return jsonify(
            {"error": "Failed to decode JSON object: " + str(e)}
        ), 400 @ app.route("/v1/api/vectorize", methods=["POST"])


@app.route("/v1/api/search", methods=["POST"])
def search():
    try:
        request_data = request.get_json()
        return controller.search(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)
