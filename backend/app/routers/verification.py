
from fastapi import APIRouter
from app.core.database import db

router = APIRouter(prefix="/verify", tags=["Verification"])

@router.post("/{waid}")
async def verify(waid: str):
    await db.waste_actions.update_one({"waid": waid}, {"$set": {"verified": True}})
    return {"verified": True}
