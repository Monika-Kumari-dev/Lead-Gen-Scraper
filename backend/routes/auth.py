from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from auth import verify_password, create_access_token, ADMIN_EMAIL

router = APIRouter()


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/login", response_model=LoginResponse)
def login(payload: LoginRequest):
    if payload.email != ADMIN_EMAIL or not verify_password(payload.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    return LoginResponse(access_token=create_access_token(payload.email))