from llama_index.core import StorageContext, Document, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.opensearch import OpensearchVectorStore

from abc import ABC, abstractmethod

from src.utils import utils


class AbstractLlamaIndexService(ABC):
    @abstractmethod
    def vector_store_index(self, twin_id, source_name, file_uuid, documents):
        pass

    @abstractmethod
    def vectorize_string(self, text_input):
        pass


class LlamaIndexService(AbstractLlamaIndexService):
    def __init__(self, vector_store: OpensearchVectorStore):
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)
        self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

    def vector_store_index(self, twin_id, source_name, file_uuid, documents):
        docs = []
        for message in documents:
            # tokenization, lower-casing, and removal of stopwords and punctuation before generating embeddings
            processed_text = utils.preprocess_text(message["text"])
            processed_user = utils.preprocess_text(message["user_name"])
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
                    }
                )
            )
        VectorStoreIndex.from_documents(
            documents=docs,
            storage_context=self.storage_context,
            embed_model=self.embed_model
        )
        return

    def vectorize_string(self, text_input):
        return self.embed_model.get_text_embedding(text_input)
