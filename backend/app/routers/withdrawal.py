from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from app.core.database import db
from app.core.security import get_current_user
from app.services.wallet_rules import is_withdrawable

router = APIRouter(prefix="/withdraw", tags=["Withdrawal"])


@router.post("")
async def withdraw(amount: float, destination: str, user_id: str = Depends(get_current_user)):
    if amount <= 0:
        raise HTTPException(400, "Amount must be greater than zero")

    if not destination.strip():
        raise HTTPException(400, "Destination is required")

    wallet = await db.wallets.find_one({"user_id": user_id})
    if not wallet:
        raise HTTPException(404, "Wallet not found")

    wallet_id = wallet.get("_id")
    ledger = await db.wallet_ledger.find({"wallet_id": wallet_id, "status": "confirmed"}).to_list(1000)
    withdrawable = sum(
        entry.get("amount", 0)
        for entry in ledger
        if entry.get("amount", 0) > 0 and is_withdrawable(entry.get("rail", ""))
    )

    if amount > withdrawable:
        raise HTTPException(400, "Insufficient balance")

    entry = {
        "entry_id": f"L-{uuid4().hex[:8]}",
        "wallet_id": wallet_id,
        "rail": "WITHDRAWAL",
        "amount": -amount,
        "status": "confirmed",
        "destination": destination.strip(),
    }
    await db.wallet_ledger.insert_one(entry)
    return {"status": "processing"}
