from logging import Logger
from typing import Any

import numpy
import numpy as np

from core.abstracts.services import AbstractOpensearchService
from core.abstracts.usescases import AbstractVectorizeUsecase
from core.service.llama_index_service import AbstractLlamaIndexService
from core.service.s3_service import AbstractS3Service

EMBED_FIELD = "embedding"


class VectorizerUsecase(AbstractVectorizeUsecase):
    """
    Usecase for vectorizing and indexing documents.
    """

    def __init__(
        self,
        s3_service: AbstractS3Service,
        llama_index_service: AbstractLlamaIndexService,
        opensearch_service: AbstractOpensearchService,
        logger: Logger,
    ):
        """
        Initialize the Usecase.

        Args:
            s3_service (AbstractS3Service): An instance of a class implementing the AbstractS3Service interface.
            llama_index_service (AbstractLlamaIndexService): An instance of a class implementing the AbstractLlamaIndexService interface.
        """
        self.s3_service = s3_service
        self.llama_index_service = llama_index_service
        self.opensearch_service = opensearch_service
        self.logger = logger

    def vectorize_and_index(self, bucket_name: str, object_key: str) -> str:
        """
        This method retrieves JSON content from the specified S3 bucket and delegates indexing tasks
        to the llama_index_service.

        Args:
            bucket_name (str): Name of the S3 bucket containing the document.
            object_key (str): Key of the document object in the S3 bucket.

        Returns:
            str: The indexed document.
        """

        json_content = self.s3_service.get_object(bucket_name, object_key)
        self.logger.info(f"Received vectorization request for {object_key}")
        if json_content is None:
            error_message = "Not content to be indexing"
            self.logger.error(error_message)
            raise ValueError(error_message)
        try:
            twin_id, source_name, channel, file_uuid = object_key.split("/")
            return self.llama_index_service.vector_store_index(
                twin_id, source_name, channel, file_uuid, json_content
            )
        except ValueError as e:
            self.logger.error(e)
            raise ValueError(e)

    def search(self, query: str) -> list[dict[str, Any]]:
        """
        Performs a search request to the configured opensearch index. Returns a list of results
        Args:
            query (str): the string to search in the indexed documents

        Returns:
            list[dict[str, Any]]: A list of matching documents.
        """
        # vectorize query
        v_query = self.llama_index_service.vectorize_string(query)
        vector = np.array(v_query)
        # build query
        query = build_opensearch_vector_query(vector, EMBED_FIELD)
        # search and return results
        results = self.opensearch_service.search(query)
        messages = [
            {
                "raw_text": result["_source"]["metadata"]["raw_text"],
                "source_name": result["_source"]["metadata"]["source_name"],
                "file_uuid": result["_source"]["metadata"]["file_uuid"],
            }
            for result in results
        ]
        return messages


def build_opensearch_vector_query(
    query_vector: numpy.ndarray, field_name: str, k: int = 10
) -> dict:
    """
    Builds an OpenSearch query for searching in vector fields sorted by cosine similarity.
    Args:
        query_vector (numpy.ndarray): The vectorized representation of the input query.
        field_name (str): The name of the knn_vector field in your OpenSearch index.
        k (int, optional): The number of nearest neighbors to return. Defaults to 10.
    Returns:
        dict: An OpenSearch query dictionary.
    """

    query = {
        "size": k,
        "query": {
            "script_score": {
                "query": {"match_all": {}},
                "script": {
                    "source": "cosineSimilarity(params.query_vector, doc['{}']) + 1.0".format(
                        field_name
                    ),
                    "params": {"query_vector": query_vector.tolist()},
                },
            }
        },
    }

    return query
