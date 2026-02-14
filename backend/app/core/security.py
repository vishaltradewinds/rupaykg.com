
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

security = HTTPBearer()
ALGORITHM = "HS256"

def create_access_token(user_id: str):
    payload = {"sub": user_id, "exp": datetime.utcnow() + timedelta(hours=24)}
    return jwt.encode(payload, settings.JWT_SECRET, algorithm=ALGORITHM)

def get_current_user(creds: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(creds.credentials, settings.JWT_SECRET, algorithms=[ALGORITHM])
        return payload["sub"]
    except JWTError:
        raise HTTPException(401, "Invalid token")
