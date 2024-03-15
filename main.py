from abc import ABC, abstractmethod
from os import environ
from dotenv import load_dotenv

from flask import Flask, jsonify

from config import DevelopmentConfig, Config
from controller.controller import Controller
from service.llama_index_service import LlamaIndexService
from service.opensearch_service import OpensearchService
from service.s3_service import S3Service
from usecase.usecase import Usecase

load_dotenv()
IS_LOCAL = "IS_LOCAL"

app = Flask(__name__)
is_local = environ.get(IS_LOCAL)
cfg = Config

if is_local:
    cfg = DevelopmentConfig

app.config.from_object(cfg)

opensearch_url = f"{cfg.OPENSEARCH_HOST}:{cfg.OPENSEARCH_PORT}"
if cfg.OPENSEARCH_USE_SSL:
    opensearch_url = f"https://{opensearch_url}"
else:
    opensearch_url = f"http://{opensearch_url}"

print(opensearch_url)
# Initialize services and dependencies
s3_service = S3Service(cfg.S3_URL)
opensearch_service = OpensearchService(
    cfg.OPENSEARCH_HOST,
    cfg.OPENSEARCH_PORT,
    cfg.OPENSEARCH_USER,
    cfg.OPENSEARCH_PASSWORD,
    cfg.OPENSEARCH_USE_SSL,
    cfg.OPENSEARCH_VERIFY_CERTS,
    cfg.OPENSEARCH_INDEX,
)
llama_service = LlamaIndexService(opensearch_url, cfg.OPENSEARCH_INDEX)
usecase = Usecase(s3_service, llama_service, opensearch_service)
controller = Controller(usecase)

# Add the route
app.add_url_rule('/v1/api/vectorize', 'vectorize', controller.vectorize, methods=['POST'])
app.add_url_rule('/v1/api/search', 'search', controller.search, methods=['GET'])


if __name__ == '__main__':
    app.run(debug=True)
