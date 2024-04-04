from abc import ABC, abstractmethod
import numpy as np

from src.service.opensearch_service import AbstractOpensearchService
from src.service.s3_service import AbstractS3Service
from src.service.llama_index_service import AbstractLlamaIndexService
from src.utils.logger import logger

EMBED_FIELD = "embedding"


class AbstractUsecase(ABC):
    @abstractmethod
    def vectorize_and_index(self, bucket_name, object_key):
        pass

    @abstractmethod
    def search(self, query):
        pass


class Usecase(AbstractUsecase):
    def __init__(self,
                 s3_service: AbstractS3Service,
                 llama_index_service: AbstractLlamaIndexService,
                 opensearch_service: AbstractOpensearchService,
                 ):
        self.s3_service = s3_service
        self.llama_index_service = llama_index_service
        self.opensearch_service = opensearch_service

    def vectorize_and_index(self, bucket_name, object_key):
        json_content = self.s3_service.get_object(bucket_name, object_key)
        if json_content is None:
            logger.info("no documents to index")
            return
        try:
            twin_id, source_name, file_uuid = object_key.split("/")
        except ValueError as e:
            logger.error(f"Error while extracting 'twin_id', 'source_name', 'file_uuid' from object key: {str(e)}")
            return
        self.llama_index_service.vector_store_index(twin_id, source_name, file_uuid, json_content)
        return

    def search(self, query):
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
            } for result in results]
        return messages


def build_opensearch_vector_query(query_vector, field_name, k=10):
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
                    "source": "cosineSimilarity(params.query_vector, doc['{}']) + 1.0".format(field_name),
                    "params": {"query_vector": query_vector.tolist()}
                }
            }
        }
    }

    return query
