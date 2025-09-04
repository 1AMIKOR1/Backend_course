from typing import TypeVar

from pydantic import BaseModel

from src.database import Base


ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)

class DataMapper:
    db_model: type[ModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_model(cls, data):
        return cls.db_model(**data.model_dump())
    @classmethod
    def map_to_schema(cls, data):
        return cls.schema.model_validate(data, from_attributes=True)