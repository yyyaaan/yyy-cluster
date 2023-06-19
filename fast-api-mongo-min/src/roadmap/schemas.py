# Yan Pan
from pydantic import BaseModel
from typing import Optional, Union


class BaseOrmModel(BaseModel):
    """
    Wrapping class for support of DB ORM (obj.item dot notation)
    """
    class Config:
        orm_mode = True


class SchemaIdOnly(BaseOrmModel):
    id: Union[str, int]


class _RoadMapItem(BaseOrmModel):
    title: str
    seq: int
    description: str
    state: int


class SchemaRoadMap(BaseOrmModel):
    title: str
    seq: int
    description: str
    state: int = 0
    items: Optional[list[_RoadMapItem]]


