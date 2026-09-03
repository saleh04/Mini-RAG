from controllers.BaseController import BaseController # noqa: N999

from helpers.config import Settings  
from .providers import QdrantDB
from .VectorDBEnums import VectorDBEnums


class VectorDBProviderFactory:
    def __init__(self, config: Settings):
        self.config = config
        self.BaseController = BaseController()
        
    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.BaseController.get_database_path(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD
            )

        return None


