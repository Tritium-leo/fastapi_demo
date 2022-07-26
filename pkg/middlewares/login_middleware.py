from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from pkg import codes
from pkg.help.user_helper import UserHelper
from pkg.utils.jwt_util import check_token


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        url = request.url

        token = Request.cookies.getter("X-TOKEN")
        refresh_token = Request.cookies.getter("X-TOKEN-REFRESH")
        have_token = False
        token_time_out = False
        user_base_info = None
        if token and check_token(token):
            have_token = True
            user_base_info = check_token(token)
        elif refresh_token and check_token(refresh_token):
            have_token = True
            token_time_out = True
            user_base_info = check_token(token)

        if have_token:
            uuid, username = user_base_info["uuid"], user_base_info["username"]
            response = await call_next(request)
            if token_time_out:
                response = UserHelper.set_token(user_base_info, response)
            return user_base_info
        elif any([x in url for x in ['/login', '/register', '/verification_code']]):
            return await call_next(request)
        return JSONResponse({"code": codes.Unauthorized, "msg": "your must login to view this page"})
