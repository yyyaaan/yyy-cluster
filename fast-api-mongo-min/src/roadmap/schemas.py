# Yan Pan
from pydantic import BaseModel, Field
from typing import Optional, Union


class BaseOrmModel(BaseModel):
    """
    Wrapping class for support of DB ORM (obj.item dot notation)
    """
    class Config:
        orm_mode = True


class SchemaIdOnly(BaseOrmModel):
    id: Union[str, int]
    raw: Optional[Union[str, dict, int]]


class _RoadMapItem(BaseOrmModel):
    id: Union[str, int] = Field(alias='_id')
    title: str
    description: str
    state: int = 0
    href: Optional[str]


class SchemaRoadMap(BaseOrmModel):
    """
    mongodb uses bson.objectid.ObjectId as _id
    to avoid any confusion, id (str or int) to be provided and use as _id
    xxx.dict(by_alias=True)
    """
    id: Union[str, int] = Field(alias='_id')
    title: str
    description: str
    state: int = 0
    items: Optional[list[_RoadMapItem]]