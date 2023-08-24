from fastapi import APIRouter, Request
from motor.motor_asyncio import AsyncIOMotorCollection


router = APIRouter()


async def find_profile_or_default(
    operator: AsyncIOMotorCollection,
    filters: dict,
    add_profiles: bool = False
):
    """helper function to find matched item from DB"""
    try:
        result = await operator.find_one(filters)
        if (not result) and (filters.get("profile", "default") != "default"):
            filters["profile"] = "default"
            result = await operator.find_one(filters)

        content = result.get("content", {})

        # if list, check if ordering or filtering is necessary
        if isinstance(content, dict):
            for k in content.keys():
                if isinstance(content[k], list):
                    content[k] = sorted(
                        [x for x in content[k] if x.get("enabled", True)],
                        key=lambda x: x.get("order", 0)
                    )

        # recursively pull itemRef
        for one in content.get("mainContent", []):
            if one.get("itemsRef", False):
                one["items"] = [
                    x for x in [(
                        (await operator.find_one({"_id": x})) or {}
                    ).get("content", {}) for x in one["itemsRef"]
                    ] if len(x)
                ]

        if not add_profiles:
            return content
        return {
            "profiles": await operator.distinct("profile"),
            **content
        }
    except Exception as e:
        print(e)
        return {}


@router.get("/personal")
async def get_about_fixture(request: Request, profile: str = "default"):
    """provide data for /about page"""
    return await find_profile_or_default(
        operator=request.app.mongodb["aboutme"],
        filters={"profile": profile, "scope": "personal"},
        add_profiles=True
    )


@router.get("/contexts")
async def get_about_summary(request: Request, profile: str = "default"):
    """provide data for summary page (html)"""
    return await find_profile_or_default(
        operator=request.app.mongodb["aboutme"],
        filters={"profile": profile, "scope": "contexts"},
    )


@router.get("/certs")
async def get_about_certs(request: Request, profile: str = "default"):
    """provide data for summary page (html)"""
    return await find_profile_or_default(
        operator=request.app.mongodb["aboutme"],
        filters={"profile": profile, "scope": "certs"},
    )
