from logging import Logger

from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import OpensearchVectorStore

from core.abstracts.services import AbstractLlamaIndexService
from core.utils import utils

# OpenSearchVectorClient stores text in this field by default
TEXT_FIELD = "content"
# OpenSearchVectorClient stores embeddings in this field by default
EMBEDDING_FIELD = "embedding"


class LlamaIndexService(AbstractLlamaIndexService):
    """
    Service for indexing documents and retrieving vectors from OpenSearch.
    """

    def __init__(
            self,
            vector_store: OpensearchVectorStore,
            logger: Logger,
    ):
        """
        Initialize the LlamaIndexService.

        Args:
            vector_store (OpensearchVectorStore): Elasticsearch/Opensearch vector store instance
            logger (Logger): Logger instance.
        """
        self.logger = logger

        self.logger.info("Initializing LlamaIndexService...")
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def vector_store_index(
            self, twin_id: str, source_name: str, file_uuid: str, documents: list
    ) -> str:
        """
        Index documents and store vectors in OpenSearch.

        Args:
            twin_id (str): Identifier for the twin.
            source_name (str): Name of the data source.
            file_uuid (str): UUID of the file containing the documents.
            documents (list): list of dictionary representing documents.

        Returns:
            str: Index summary
        """
        docs = []
        for message in documents:
            # tokenization, lower-casing, and removal of stopwords and punctuation before generating embeddings
            processed_text = utils.preprocess_text(message["text"])
            processed_user = utils.preprocess_text(message["user_name"])
            embed_value = self.embed_model.get_text_embedding(processed_text)
            docs.append(
                Document(
                    text=processed_text,
                    id=message["created_at"],
                    metadata={
                        "raw_text": message["text"],
                        "user_name": message["user_name"],
                        "processed_user": processed_user,
                        "twin_id": twin_id,
                        "source_name": source_name,
                        "file_uuid": file_uuid,
                    },
                    metadata_seperator=":",
                    embedding=embed_value,
                )
            )
        self.logger.info(docs)
        try:
            index = VectorStoreIndex.from_documents(
                documents=docs,
                storage_context=self.storage_context,
                embed_model=self.embed_model,
            )
            self.logger.info(
                f"Indexing documents for {twin_id}/{source_name}/{file_uuid}: {index.summary}"
            )
            return index.summary
        except Exception as e:
            message_error = f"Error while indexing documents for {twin_id}/{source_name}/{file_uuid}"
            self.logger.error(e)
            raise ValueError(message_error)

    def vectorize_string(self, text_input: str) -> list:
        """
        Retrieves the embedded value (vector) for the text_input string

        Args:
            text_input (str): Text to vectorize

        Returns:
            list: a list of float values representing the text_input vector
        """
        return self.embed_model.get_text_embedding(text_input)
