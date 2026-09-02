import logging

from models.db_schemes import DataChunk, Project  # noqa: N999
from stores.llm.LLMEnums import DocumentTypeEnum

from .BaseController import BaseController


class NLPController(BaseController):

    def __init__(self, vectordb_client, generation_client, embedding_client):
        super().__init__()
        self.logger = logging.getLogger(__name__)
        self.vectordb_client = vectordb_client
        self.generation_client = generation_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id: str):
        return f"collection_{project_id}".strip()

    def reset_vector_db_collection(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.delete_collection(collection_name=collection_name)

    def get_vector_db_collection_info(self, project: Project):
        collection_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_client.get_collection_info(collection_name=collection_name)

    def index_into_vector_db(self, project: Project, chunks: list[DataChunk], do_reset: bool, batch_size: int = 64):

        collection_name = self.create_collection_name(project_id=project.project_id)

        texts = [c.chunk_text for c in chunks]
        metadata = [c.chunk_metadata for c in chunks]

        _ = self.vectordb_client.create_collection(collection_name=collection_name,
                                            embedding_size=self.embedding_client.embedding_size,
                                            do_reset=do_reset)

        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            batch_metadata = metadata[i:i + batch_size]

            batch_vectors = self.embedding_client.embed_batch_texts(
                texts=batch_texts, 
                document_type=DocumentTypeEnum.DOCUMENT.value
            )

            if not batch_vectors:
                self.logger.error(f"Failed to embed batch from index {i} to {i + batch_size}")
                return False

            _ = self.vectordb_client.insert_many(
                collection_name=collection_name,
                texts=batch_texts,
                vectors=batch_vectors,
                metadata=batch_metadata
            )

        return True

    def search_in_vector_db(self, project: Project, query: str, limit: int = 5):

        collection_name = self.create_collection_name(project_id=project.project_id)

        vector = self.embedding_client.embed_text(text=query, document_type=DocumentTypeEnum.QUERY.value)

        if not vector or len(vector) == 0:
            return False

        search_results = self.vectordb_client.search_by_vector(
            collection_name=collection_name,
            vector=vector,
            limit=limit
        )

        if not search_results:
            self.logger.error(f"Failed to search in vector DB for query: {query}")
            return False

        return search_results
