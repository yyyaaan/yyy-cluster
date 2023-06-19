from fastapi import APIRouter, HTTPException, Request
from templates.override import TEMPLATES_ALT
from typing import Union

from roadmap.schemas import SchemaRoadMap, SchemaIdOnly

router = APIRouter()


@router.get("/",)
async def index(request:Request):
    """
    rendered roadmap view, modifiers: [[delimiter]], {{VueJS}}
    """
    return TEMPLATES_ALT.TemplateResponse("roadmap.html", context={"request": request})


@router.get("/list")  # response_model=list[schemas.OutputRoadMapWithItems])
async def list_roadmaps(request: Request):
    """
    list all saved list_roadmaps
    """
    results = await request.app.collection_roadmap.find().to_list(length=None)
    return results


@router.post("/create", response_model=SchemaIdOnly, status_code=201)
async def create_a_new_roadmap(request: Request, roadmap: SchemaRoadMap):
    """
    create a new roadmap with items\n
    id must be provided and it is to be used as unique identifier (_id)
    """
    saved_roadmap = await request.app.collection_roadmap.insert_one(
        roadmap.dict(by_alias=True)
    )
    return {"id": str(saved_roadmap.inserted_id)}


@router.delete("/delete/{roadmap_id}", response_model=SchemaIdOnly, status_code=202)
async def delete_roadmap_by_id(request: Request, roadmap_id: Union[str, int]):
    """
    delete a roadmap by id
    """
    result = await request.app.collection_roadmap.delete_one({"_id": roadmap_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Roadmap not found")
    return {"id": roadmap_id, "raw": result.raw_result}
