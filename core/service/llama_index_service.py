from logging import Logger

from llama_index.core import Document, StorageContext, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import (
    OpensearchVectorClient,
    OpensearchVectorStore,
)

from core.abstracts.services import AbstractLlamaIndexService
from core.utils import utils

# OpenSearchVectorClient stores text in this field by default
TEXT_FIELD = "content"
# OpenSearchVectorClient stores embeddings in this field by default
EMBEDDING_FIELD = "embedding"


class LlamaIndexService(AbstractLlamaIndexService):
    def __init__(
        self,
        open_search_url: str,
        open_search_index: str,
        open_search_user: str,
        open_search_password: str,
        logger: Logger,
    ):
        """
        Initialize the LlamaIndexService.

        Args:
            open_search_url (str): URL of the OpenSearch instance.
            open_search_index (str): Name of the index in OpenSearch where vectors are stored.
            logger (Logger): Logger instance.
        """
        self.logger = logger

        self.logger.info("Initializing LlamaIndexService...")
        self.client = OpensearchVectorClient(
            endpoint=open_search_url,
            index=open_search_index,
            dim=384,
            embedding_field=EMBEDDING_FIELD,
            text_field=TEXT_FIELD,
            http_auth=(open_search_user, open_search_password),
        )

        self.vector_store = OpensearchVectorStore(self.client)
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def vector_store_index(self, twin_id, source_name, file_uuid, documents) -> str:
        """
        Index documents and store vectors in OpenSearch.

        Args:
            twin_id (str): Identifier for the twin.
            source_name (str): Name of the data source.
            file_uuid (str): UUID of the file containing the documents.
            documents (list): List of dictionaries representing documents.

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
