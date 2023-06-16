from fastapi import APIRouter, Depends, Request
from utils.templating import TEMPLATES_ALT

from roadmap import schemas

router = APIRouter()


@router.get("/",)
async def index(request:Request):
    # return {"info": "FastAPI ready", "templates": "Jinja2 modified [[delimiter]] , VueJS normal {{delimiter}."}
    return TEMPLATES_ALT.TemplateResponse("index.html",context={"request":request})

@router.get("/roadmap")
async def index(request:Request):
    return TEMPLATES_ALT.TemplateResponse("roadmap.html",context={"request":request})

@router.get("/api/roadmap", response_model=list[schemas.OutputRoadMapWithItems]) #
async def get_roadmaps():
    return {}

@router.post("/add-roadmap", response_model=schemas.SchemaIdOnly, status_code=201)
async def create_roadmap(request: Request, roadmap: schemas.SchemaRoadMap):
    saved_roadmap = await request.app.mongodb["roadmaps"].insert_one(roadmap.dict())
    return saved_roadmap

@router.post("/api/roadmap/item", response_model=schemas.SchemaIdOnly, status_code=201)
async def create_roadmap_item(roadmap_item: schemas.SchemaRoadMapItem):
    return {}

@router.delete("/api/roadmap/{roadmap_id}", response_model=schemas.SchemaIdOnly, status_code=202)
async def delete_roadmap(roadmap_id: int):
    return {}

