from bson.objectid import ObjectId
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Project(BaseModel):
    id: ObjectId | None = Field(None, alias="_id")
    project_id: str = Field(..., min_length=1)

    @field_validator("project_id")
    @classmethod
    def validate_project_id(cls, value):
        if not value.isalnum():
            raise ValueError('project_id must be alphanumeric')

        return value

    model_config = ConfigDict(arbitrary_types_allowed=True)

    @classmethod
    def get_index(cls):
        return [
            {
                'key':[
                    ("project_id", 1)
                ],
                'name': 'project_id_index_1',
                'unique': True
            }
        ]