from fastapi import APIRouter, Depends, HTTPException
from controllers import weather

router = APIRouter()

router.include_router(
    router,
    prefix="/api")

