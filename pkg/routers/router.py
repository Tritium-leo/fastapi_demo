from fastapi import APIRouter

v1 = APIRouter(prefix="/v1", tags=["v1"])
v2 = APIRouter(prefix="/v2", tags=["v2"])

from pkg.service.user_service import *