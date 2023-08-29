from fastapi import APIRouter, HTTPException, Request
from typing import Union

from roadmap.schemas import SchemaRoadMap, SchemaIdOnly

router = APIRouter()


@router.get("/list", response_model=list[SchemaRoadMap])
async def list_roadmaps(request: Request):
    """
    list all saved list_roadmaps
    """
    results = await request.app.collection_roadmap.find(
        {"state": 1}, {}
    ).to_list(length=None)
    results.sort(key=lambda x: str(x.get("order", 999)))
    return results


@router.post("/create", response_model=SchemaIdOnly, status_code=201)
async def create_a_new_roadmap(request: Request, roadmap: SchemaRoadMap):
    """
    create a new roadmap with items\n
    id must be provided and it is to be used as unique identifier (_id)
    """
    try:
        params = roadmap.model_dump(by_alias=True)
    except:  # noqa: E722
        params = roadmap.dict(by_alias=True)  # pydantic backward compatibility
    saved_roadmap = await request.app.collection_roadmap.insert_one(
        params
    )
    return {"id": str(saved_roadmap.inserted_id)}


@router.delete("/delete/{roadmap_id}",
               response_model=SchemaIdOnly, status_code=202)
async def delete_roadmap_by_id(request: Request, roadmap_id: Union[str, int]):
    """
    delete a roadmap by id
    """
    result = await request.app.collection_roadmap.delete_one(
        {"_id": roadmap_id}
    )
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return {"id": roadmap_id, "raw": result.raw_result}
