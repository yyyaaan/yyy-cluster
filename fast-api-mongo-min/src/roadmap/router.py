from fastapi import APIRouter, HTTPException, Request
from utils.templating import TEMPLATES_ALT
from typing import Union

from roadmap.schemas import SchemaRoadMap, SchemaIdOnly

router = APIRouter()


@router.get("/",)
async def index(request:Request):
    """
    rendered roadmap view
    """
    # return {"info": "FastAPI ready", "templates": "Jinja2 modified [[delimiter]] , VueJS normal {{delimiter}."}
    return TEMPLATES_ALT.TemplateResponse("index.html",context={"request":request})

@router.get("/list")#, response_model=list[schemas.OutputRoadMapWithItems]) #
async def list_roadmaps(request: Request):
    """
    list all saved list_roadmaps
    """
    results = []
    for one in  await request.app.collection_roadmap.find().to_list(length=100):
        one["_id"] = str(one["_id"])
        results.append(one)
    return results


@router.post("/create", response_model=SchemaIdOnly, status_code=201)
async def create_a_new_roadmap(request: Request, roadmap: SchemaRoadMap):
    """
    create a new roadmap, i.e. a container of many steps
    """
    saved_roadmap = await request.app.collection_roadmap.insert_one(roadmap.dict())
    return {"id": str(saved_roadmap.inserted_id)}


@router.delete("/delete/{roadmap_id}", response_model=SchemaIdOnly, status_code=202)
async def delete_roadmap_by_id(roadmap_id: Union[str, int]):
    """
    delete a roadmap by id
    """
    await request.app.collection_roadmap.delete_one({"_id": roadmap_id})
    return {"id": roadmap_id}


