from pkg.dao.mysql import engien
from pkg.dao.user import *
from pkg.dao.redis import redis_cli
from pkg.model.constant import UserRedisInfoCacheKey, UserQueryBatchMax
from pkg.codes.code import *

import json


class UserHelper:
    @classmethod
    def get_user_by_name(cls, username) -> Dict:
        # illegal value filter
        if not User.check_username(username):
            return None

        v = redis_cli.hget(UserRedisInfoCacheKey, username)
        if v is not None:
            return json.loads(v)
        UserHelper.fetch_user()

    @classmethod
    def fetch_users(cls, user_ids: List[int]) -> Dict[str, Any]:
        if len(user_ids) > UserQueryBatchMax:
            raise Exception(REQUEST_ERROR)
        users = redis_cli.hmget(UserRedisInfoCacheKey, *user_ids)
        exist_ids = [x.get("uuid") for x in users]
        diff_ids = [x for x in user_ids if x["uuid"] not in exist_ids]
        if not diff_ids:
            return users
        db = get_db()
        users = db.query(User).filter(User.uuid.in_(user_ids)).all()
        update_data = {}
        for u in users:
            update_data[u.usename] = u.to_dict()
            update_data[u.uuid] = u.to_dict()
        redis_cli.hmset(UserRedisInfoCacheKey, update_data)
        return [x.to_dict() for x in users]

    @classmethod
    def fetch_user(cls, user_id: int) -> Dict[str, Any]:
        u = redis_cli.hget(UserRedisInfoCacheKey, user_id)
        if u is not None:
            return u
        db = get_db()
        user = db.query(User).filter(User.uuid == user_id).one()
        if user is None:
            return
        redis_cli.hset(UserRedisInfoCacheKey, user.username, user.to_dict())
        redis_cli.hset(UserRedisInfoCacheKey, user.uuid, user.to_dict())
        return user.to_dict()

    @classmethod
    def fetch_user_by_name(cls, username: int) -> Dict[str, Any]:
        db = get_db()
        user = db.query(User).filter(User.username == username).one()
        if user is None:
            return
        redis_cli.hset(UserRedisInfoCacheKey, user.username, user.to_dict())
        return user.to_dict()

    # @classmethod
    # def hot_load(self):
    #     conn = engien.connect()
    #     sql = "select * from user order by last_login_time"
    #     conn.execute()
