import unittest
from http import HTTPStatus
from unittest.mock import patch, MagicMock  # For mocking dependencies
from src.controller import controller
from test.conftest import app, client
from src.usecase.usecase import AbstractUsecase


class TestController(unittest.TestCase):

    def setUp(self):
        self.mock_usecase = MagicMock(spec=AbstractUsecase)  # Create a mock usecase
        self.controller = controller.Controller(self.mock_usecase)
        self.app = app()
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = client(self.app)

        # Test cases for 'vectorize' will go here
    @patch('flask.request')
    def test_vectorize_success(self, mock_request):
        response = self.client.post('/', json={
            'Records': [{'s3': {'bucket': {'name': 'bucket_name'},
                                'object': {'key': 'object_key'}}}]
        })

        self.mock_usecase.vectorize_and_index.assert_called_once_with('bucket_name', 'object_key')

    # Test cases for 'search' will go here
    @patch('flask.request')
    def test_search_success(self, mock_request):
        mock_request.method = 'GET'
        mock_request.args.get = MagicMock(return_value="test_query")
        self.mock_usecase.search.return_value = ['result1', 'result2']

        response = self.controller.search()

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response.json, {'results': ['result1', 'result2']})
        self.mock_usecase.search.assert_called_once_with('test_query')


if __name__ == '__main__':
    unittest.main()
