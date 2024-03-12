from abc import ABC, abstractmethod
from os import environ
from dotenv import load_dotenv

from flask import Flask, jsonify

from config import DevelopmentConfig, Config
from controller.controller import Controller
from service.s3_service import S3Service
from usecase.usecase import Usecase
from utils.logger import logger

load_dotenv()
IS_LOCAL = "IS_LOCAL"

app = Flask(__name__)
is_local = environ.get(IS_LOCAL)
cfg = Config

if is_local:
    cfg = DevelopmentConfig

app.config.from_object(cfg)


# Initialize services and dependencies
s3_service = S3Service()
usecase = Usecase(s3_service)
controller = Controller(usecase)

# Add the route
app.add_url_rule('/v1/api/vectorize', 'vectorize', controller.vectorize, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)
