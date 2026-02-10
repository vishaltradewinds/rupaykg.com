
from fastapi import APIRouter, Depends, HTTPException
from uuid import uuid4
from app.core.security import get_current_user
from app.core.database import db
from app.services.wallet_rules import is_withdrawable

router = APIRouter(prefix="/withdraw", tags=["Withdrawal"])

@router.post("")
async def withdraw(amount: float, destination: str, user_id: str = Depends(get_current_user)):
    wallet = await db.wallets.find_one({"user_id": user_id})
    ledger = await db.wallet_ledger.find({"wallet_id": wallet["_id"], "status": "confirmed"}).to_list(1000)
    withdrawable = sum(e["amount"] for e in ledger if e["amount"] > 0 and is_withdrawable(e["rail"]))
    if amount > withdrawable:
        raise HTTPException(400, "Insufficient balance")
    entry = {
        "entry_id": f"L-{uuid4().hex[:8]}",
        "wallet_id": wallet["_id"],
        "rail": "WITHDRAWAL",
        "amount": -amount,
        "status": "confirmed"
    }
    await db.wallet_ledger.insert_one(entry)
    return {"status": "processing"}
