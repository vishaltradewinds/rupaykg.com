from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import auth, verification, wallet, waste, withdrawal

app = FastAPI(title="RupayKg API", version="1.0.0")

allowed_origins = [origin.strip() for origin in settings.BACKEND_CORS_ORIGINS.split(",") if origin.strip()]
allow_all_origins = allowed_origins == ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if allow_all_origins else allowed_origins,
    allow_credentials=not allow_all_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    if settings.SYSTEM_STATUS != "ACTIVE":
        raise HTTPException(503, "System paused")
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(waste.router)
app.include_router(verification.router)
app.include_router(wallet.router)
app.include_router(withdrawal.router)
