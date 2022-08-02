from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware

from pkg import codes


class ErrorMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):

        try:
            response = await call_next(request)
        except Exception as e:
            logger.error(
                f"Method:[{request.method}] Url:[{request.url}] \n" +
                f"Header:{request.headers} \n" +
                f"PathParam:{request.path_params} \n" +
                f"QueryParams:{request.query_params} \n" +
                # f"Json:{await request.json()} \n" +
                # f"Body:{await request.body()} \n" +
                f"ERROR:{e}"
            )
            logger.exception(e)
            return JSONResponse({"code": codes.INTERNAL_SERVICE_ERROR, "msg": str(e)})
        else:

            return response
