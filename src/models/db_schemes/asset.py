from datetime import datetime

from bson.objectid import ObjectId
from pydantic import BaseModel, ConfigDict, Field


class Asset(BaseModel):
    id: ObjectId | None = Field(None, alias="_id")
    asset_project_id: ObjectId
    asset_type: str = Field(...,min_length=1)
    asset_name: str = Field(...,min_length=1)
    asset_size: int = Field(ge=0, default=None)
    asset_pushed_at: datetime = Field(default=datetime.utcnow)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_index(cls):
        return [
            {
                'key':[
                    ("asset_project_id", 1)
                ],
                'name': 'asset_project_id_index_1',
                'unique': False
            },
            {
                'key':[
                    ("asset_project_id", 1),
                    ("asset_name", 1)
                ],
                'name': 'asset_project_id_name_index_1',
                'unique': True
            }
        ]