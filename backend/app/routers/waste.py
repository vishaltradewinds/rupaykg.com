
from fastapi import APIRouter
from uuid import uuid4
from app.core.database import db

router = APIRouter(prefix="/waste", tags=["Waste"])

@router.post("")
async def create_waste(payload: dict):
    payload["waid"] = f"WA-{uuid4().hex[:8]}"
    payload["verified"] = False
    await db.waste_actions.insert_one(payload)
    return payload
