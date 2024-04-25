from dotenv import load_dotenv
from flask import Flask, jsonify, request

from config import IS_LOCAL, Config, DevelopmentConfig
from core.controller.vector import VectorController
from core.service.llama_index_service import LlamaIndexService
from core.service.s3_service import S3Service
from core.usecase.vectorizer import VectorizerUsecase
from core.utils.logger import logger

load_dotenv()

cfg = DevelopmentConfig if IS_LOCAL else Config

app = Flask(__name__)
app.config.from_object(cfg)


# Initialize services and dependencies
s3_service = S3Service(cfg.S3_URL, logger)
llama_service = LlamaIndexService(
    cfg.OPENSEARCH_CLUSTER_URL,
    cfg.OPENSEARCH_INDEX,
    cfg.OPENSEARCH_USER,
    cfg.OPENSEARCH_PASS,
    logger,
)
usecase = VectorizerUsecase(s3_service, llama_service, logger)
controller = VectorController(usecase, logger)


@app.route("/v1/api/vectorize", methods=["POST"])
def vectorize():
    try:
        request_data = request.get_json()
        return controller.vectoring(request_data)
    except Exception as e:
        return jsonify({"error": "Failed to decode JSON object: " + str(e)}), 400


if __name__ == "__main__":
    app.run()
