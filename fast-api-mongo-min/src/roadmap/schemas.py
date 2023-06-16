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
    id: int


class SchemaRoadMap(BaseOrmModel):
    title: str
    description: str
    state: int = 0


class SchemaRoadMapItem(BaseOrmModel):
    roadmap_id: int
    title: str
    description: str
    state: int


class OutputRoadMapWithItems(SchemaRoadMap):
    id: int
    items: list[SchemaRoadMapItem]


class OutputTBD(BaseModel):
    identifier: Optional[Union[str, int]]
    info: str


class OutputPrediction(BaseModel):
    result: Union[float, int]
    input_shape: list[int]
    wall_time: float
    model_name: str
    model_version: Union[int, str]
    model_id: str
    model_utc: str


class OutputPredictionMany(OutputPrediction): # note parent
    result: list[Union[float, int]]
