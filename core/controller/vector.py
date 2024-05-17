from http import HTTPStatus
from logging import Logger
from typing import Any, Dict, Tuple

from flask import jsonify, Response

from core.abstracts.controller import AbstractVectorController
from core.abstracts.usescases import AbstractVectorizeUsecase


class VectorController(AbstractVectorController):
    """
    Controller for vectorization operations.
    """

    def __init__(self, usecase: AbstractVectorizeUsecase, logger: Logger):
        """
        Initialize the Controller.

        Args:
            usecase (AbstractUsecase): An instance of a class implementing the AbstractUsecase interface.
        """
        self.usecase = usecase
        self.logger = logger

    def vectoring(self, request: Dict[str, Any]) -> Tuple[Response, int]:
        """
        Handle vectorization requests.

        This method expects a POST request with JSON data containing S3 bucket and object key information.
        It delegates vectorization and indexing tasks to the use case, and returns appropriate responses.

        Args:
            request (Dict[str, Any]): Request body.

        Returns:
            Tuple[Dict[str, str], int]: Tuple containing a JSON response indicating success or failure of the vectorization process and an HTTP status code.
        """
        record = request["Records"][0]["s3"]
        s3_bucket = record["bucket"]["name"]
        s3_object_key = record["object"]["key"]

        try:
            self.usecase.vectorize_and_index(s3_bucket, s3_object_key)
            return jsonify({"message": "Object vectorization succeeded!"}), HTTPStatus.OK
        except Exception as e:
            self.logger.error(f"Failed to vectorize object {s3_object_key}")
            return jsonify({"error": str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    def search(self, request: Dict[str, Any]) -> Tuple[Response, int]:
        query = request["q"]
        if query is None or query.strip() == "":
            return jsonify({'error': 'query param "q" is required'}), HTTPStatus.BAD_REQUEST

        try:
            result = self.usecase.search(query)
            return jsonify({'results': result}), HTTPStatus.OK
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
