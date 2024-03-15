from http import HTTPStatus
from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from usecase.usecase import AbstractUsecase


class AbstractController(ABC):
    @abstractmethod
    def vectorize(self):
        pass

    @abstractmethod
    def search(self):
        pass


class Controller(AbstractController):
    def __init__(self, usecase: AbstractUsecase):
        self.usecase = usecase

    def vectorize(self):
        if request.method != 'POST':
            return jsonify({'error': 'Method not allowed'}), HTTPStatus.METHOD_NOT_ALLOWED

        request_data = request.get_json()
        s3_bucket = request_data['Records'][0]['s3']['bucket']['name']
        s3_object_key = request_data['Records'][0]['s3']['object']['key']

        try:
            self.usecase.vectorize_and_index(s3_bucket, s3_object_key)
            return jsonify({'message': 'Object vectorization succeeded!'}), HTTPStatus.OK
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR

    def search(self):
        if request.method != "GET":
            return jsonify({'error': 'Method not allowed'}), HTTPStatus.METHOD_NOT_ALLOWED
        query = request.args.get("q")
        if query is None or query.strip() == "":
            return jsonify({'error': 'query param "q" is required'}), HTTPStatus.BAD_REQUEST

        try:
            result = self.usecase.search(query)
            return jsonify({'message': result}), HTTPStatus.OK
        except Exception as e:
            return jsonify({'error': str(e)}), HTTPStatus.INTERNAL_SERVER_ERROR
