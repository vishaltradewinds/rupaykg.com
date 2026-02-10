from fastapi import APIRouter, Depends, HTTPException

from app.core.database import db
from app.core.security import get_current_user
from app.services.wallet_rules import is_withdrawable

router = APIRouter(prefix="/wallet", tags=["Wallet"])


@router.get("/me")
async def wallet_me(user_id: str = Depends(get_current_user)):
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
    locked = sum(
        entry.get("amount", 0)
        for entry in ledger
        if entry.get("amount", 0) > 0 and not is_withdrawable(entry.get("rail", ""))
    )

    return {"withdrawable_balance": withdrawable, "locked_balance": locked, "ledger": ledger}
