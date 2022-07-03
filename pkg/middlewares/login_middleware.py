from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from pkg.dao import redis


class SSOMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # response = await call_next(request)
        # response.headers['Custom'] = 'Example'
        url = request.url
        if Request.cookies.getter("X-TOKEN"):
            redis.redis_cli.get("")
            pass

        if any([x in url for x in ['/login', '/register', '/ver']]):
            return await call_next(request)
        else:
            # must login before
            pass
        return response
