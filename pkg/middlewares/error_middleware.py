from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from pkg import codes


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        try:
            response = await call_next(request)
        except Exception as e:
            # TODO LOGGER request.body
            logger.exception(
                f"Method:[{request.method}] Url:[{request.url}] Param:{request.path_params if request.path_params else request.query_params} ")
            logger.exception(e)
            return JSONResponse({"code": codes.INTERNAL_SERVICE_ERROR, "msg": str(e)})
        else:
            return response
