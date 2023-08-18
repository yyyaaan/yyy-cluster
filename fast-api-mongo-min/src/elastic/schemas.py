# Yan Pan
from pydantic import BaseModel
from typing import Optional, Union


class SchemaIndicesList(BaseModel):
    """
    Schema for the indices list
    """
    indices: list[str]
    info: Optional[str] = ""


class SchemaQueryResponse(BaseModel):
    """
    Schema for the query response
    """
    took: int
    max_score: Optional[float] = 0
    total: Optional[dict] = {}
    hits: Optional[list[dict]] = []
