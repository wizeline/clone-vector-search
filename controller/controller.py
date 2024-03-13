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
        bucket_name = request_data['s3']['bucket']['name']
        object_key = request_data['s3']['object']['key']

        try:
            result = self.usecase.get_object(bucket_name, object_key)
            # TODO: Process the 'result' (content from S3) for 'vectorization'
            return jsonify({'message': 'Object vectorization in progress!', 'result': result}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
