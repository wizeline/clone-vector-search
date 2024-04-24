import http
import json
from unittest.mock import patch

from src.controller.controller import Controller


def test_vectorize_endpoint(test_app_client, mock_llama_service, mock_opensearch_service, mock_opensearch_client):
    """Test the /v1/api/vectorize endpoint"""
    with patch('src.controller.controller.current_app') as current_app_mock:
        current_app_mock.config = {"OPENSEARCH_INDEX": "test index"}

        # Inject the mock opensearch service with the mock opensearch client
        mock_opensearch_service.opensearch_client = mock_opensearch_client
        controller = Controller(mock_llama_service)
        # sample payload for testing
        payload = {
            "texts": ["Vae, omnia!", "Nutrixs tolerare in berolinum!"]
        }

        response = test_app_client.post("/v1/api/vectorize", json=payload)

        assert response.status_code == http.HTTPStatus.OK
        data = json.loads(response.data)
        print(data)


def test_search_endpoint(test_app_client, mock_opensearch_service, mock_opensearch_client):
    """Test the /v1/api/search endpoint."""
    with patch('src.controller.controller.current_app') as current_app_mock:
        current_app_mock.config = {'OPENSEARCH_INDEX': 'test_index'}

        # Inject the mock opensearch service with the mock opensearch client
        mock_opensearch_service.opensearch_client = mock_opensearch_client
        controller = Controller(mock_opensearch_service)

        # Define a sample payload for testing
        payload = {
            'query': 'example query'
        }

        # Make a POST request to the endpoint
        response = test_app_client.post('/v1/api/search', json=payload)

        # Assert the response
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'results' in data
        assert isinstance(data['results'], list)
