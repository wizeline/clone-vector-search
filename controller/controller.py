from abc import ABC, abstractmethod
from flask import Flask, request, jsonify
from usecase.usecase import AbstractUsecase


class AbstractController(ABC):
    @abstractmethod
    def vectorize(self):
        pass


class Controller(AbstractController):
    def __init__(self, usecase: AbstractUsecase):
        self.usecase = usecase

    def vectorize(self):
        if request.method != 'POST':
            return jsonify({'error': 'Method not allowed'}), 405

        request_data = request.get_json()
        s3_bucket = request_data['Records'][0]['s3']['bucket']['name']
        s3_object_key = request_data['Records'][0]['s3']['object']['key']

        try:
            self.usecase.vectorize_and_index(s3_bucket, s3_object_key)
            return jsonify({'message': 'Object vectorization succeeded!'}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
