from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from pkg import codes


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.error(e)
            return JSONResponse({"code": codes.INTERNAL_SERVICE_ERROR, "msg": str(e)})
