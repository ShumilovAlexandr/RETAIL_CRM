from fastapi import APIRouter

from . import service
from . import pagination

router = APIRouter()


router.include_router(service.router)
router.include_router(pagination.router)

