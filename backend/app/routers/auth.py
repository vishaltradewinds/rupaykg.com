
from fastapi import APIRouter
from uuid import uuid4
from app.core.database import db
from app.core.security import create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/login")
async def login(phone: str):
    user = await db.users.find_one({"phone": phone})
    if not user:
        user = {"_id": str(uuid4()), "phone": phone}
        await db.users.insert_one(user)
        await db.wallets.insert_one({"user_id": user["_id"], "available_balance": 0})
    return {"access_token": create_access_token(user["_id"])}
