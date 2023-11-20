from fastapi import APIRouter

from . import service

router = APIRouter()


router.include_router(service.router)

