
from fastapi import APIRouter, Depends
from app.core.security import get_current_user
from app.core.database import db
from app.services.wallet_rules import is_withdrawable

router = APIRouter(prefix="/wallet", tags=["Wallet"])

@router.get("/me")
async def wallet_me(user_id: str = Depends(get_current_user)):
    wallet = await db.wallets.find_one({"user_id": user_id})
    ledger = await db.wallet_ledger.find({"wallet_id": wallet["_id"], "status": "confirmed"}).to_list(1000)
    withdrawable = sum(e["amount"] for e in ledger if e["amount"] > 0 and is_withdrawable(e["rail"]))
    locked = sum(e["amount"] for e in ledger if e["amount"] > 0 and not is_withdrawable(e["rail"]))
    return {"withdrawable_balance": withdrawable, "locked_balance": locked, "ledger": ledger}
