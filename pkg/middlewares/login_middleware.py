from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from pkg import codes
from pkg.utils.jwt_util import check_payload


class SSOMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        # response = await call_next(request)
        # response.headers['Custom'] = 'Example'
        url = request.url
        token = Request.cookies.getter("X-TOKEN")
        refresh_token = Request.cookies.getter("X-TOKEN-REFRESH")
        have_token = False
        user_base_info = None
        if token and check_payload(token):
            have_token = True
            user_base_info = check_payload(token)
        elif refresh_token and check_payload(refresh_token):
            have_token = True
            user_base_info = check_payload(token)

        if have_token:
            uuid, username = user_base_info["uuid"], user_base_info["username"]
            return await call_next(request)
        elif any([x in url for x in ['/login', '/register', '/verification_code']]):
            return await call_next(request)
        return JSONResponse({"code": codes.Unauthorized, "msg": "your must login to view this page"})
