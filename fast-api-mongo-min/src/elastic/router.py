# Yan Pan, 2023
from fastapi import APIRouter, HTTPException, Request
from httpx import AsyncClient
from settings.settings import Settings

from elastic.schemas import SchemaIndicesList, SchemaQueryResponse

router = APIRouter()
ESURL = Settings().ELASTICSEARCH_URL

# auth set in main.py

@router.get("/", response_model=SchemaIndicesList)
async def list_available_indices(request: Request):
    """
    list indices from ElasticSearch backend
    """
    try:
        async with AsyncClient() as client:
            res = await client.get(url=f"{ESURL}/_aliases")
        if res.status_code > 299:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Elastic Search not available {res.text}"
            )
        indices = [k for k, _ in res.json().items() if not k.startswith(".")]
        return {"indices": indices, "info": f"available {len(indices)}"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/query", response_model=SchemaQueryResponse)
async def elastic_query(request: Request, index: str, query: str):
    """
    send simple query to Elastic Search. index should be one from /
    """
    try:
        payload = {
            "query": {"query_string": {"query": query}},
            "fields": ["@timestamp", "log"],
            "sort": [
                {"@timestamp": {"order": "desc", "format": "YYYY-MM-dd HH:mm:ss"}},  # noqa: E501
            ],
            "_source": False,
        }
        async with AsyncClient() as client:
            res = await client.post(
                url=f"{ESURL}/{index}/_search",
                json=payload
            )
        if res.status_code > 299:
            raise HTTPException(
                status_code=res.status_code,
                detail=f"Elastic Search not available {res.text}"
            )
        output = res.json()
        return {'took': output['took'], **output['hits']}

    except Exception as e:
        raise HTTPException(status_code=503, detail=str(e))
