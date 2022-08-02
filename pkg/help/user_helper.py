from typing import *

import starlette.responses

import pkg.dao.user as dao_user
from pkg import constant
from pkg.codes.code import *
from pkg.dao import redis
from pkg.model.user import User
from pkg.utils.jwt_util import get_token


class UserHelper:
    @staticmethod
    def set_token(payload, response: starlette.responses.Response) -> starlette.responses.Response:
        token = get_token(payload, px=constant.user.UserTokenDuration)
        refresh_token = get_token(payload, px=constant.user.UserTokenDuration * 2)

        response.set_cookie("X-TOKEN", token)
        response.set_cookie("X-TOKEN-REFRESH", refresh_token)
        return response

    @staticmethod
    def fetch_users(user_ids: List[int]) -> List[User]:
        if len(user_ids) > constant.user.UserQueryBatchMax:
            raise Exception(REQUEST_ERROR)
        users = redis.client.hmget(constant.user.UserRedisInfoCacheKey, *user_ids)
        users = [User(**x) for x in users]
        exist_ids = [x.uuid for x in users]
        diff_ids = [x for x in user_ids if x not in exist_ids]
        if not diff_ids:
            return users
        users = dao_user.fetch_users(user_ids)
        # save redis
        update_data = {}
        for u in users:
            update_data[u.usename] = u.to_dict()
            update_data[u.uuid] = u.to_dict()
        redis.client.hmset(constant.user.UserRedisInfoCacheKey, update_data)
        return users

    @staticmethod
    def fetch_user(user_id: int) -> Union[User, None]:
        with redis.client.get_cli() as cli:
            u = cli.hget(constant.user.UserRedisInfoCacheKey, str(user_id))
            if u is not None:
                return u
        user = dao_user.fetch_user(user_id=user_id)
        if user is None:
            return
        with redis.client.get_cli() as cli:
            cli.hset(constant.user.UserRedisInfoCacheKey, user.username, user.to_dict())
            cli.hset(constant.user.UserRedisInfoCacheKey, user.uuid, user.to_dict())
        return user

    @staticmethod
    def fetch_user_by_name(username: str) -> Union[User, None]:
        # illegal value filter
        if not User.check_username(username):
            return None
        with redis.client.get_cli() as cli:
            u = cli.hget(constant.user.UserRedisInfoCacheKey, username)
            u = redis.client.try_parse_dict(u)
            if u is not None:
                return User(**u)
        user = dao_user.fetch_user(username=username)
        if user is None:
            return

        redis.client.hset(constant.user.UserRedisInfoCacheKey, user.username, user.to_dict())
        return user

    # @classmethod
    # def hot_load(self):
    #     conn = engien.connect()
    #     sql = "select * from user order by last_login_time"
    #     conn.execute()
