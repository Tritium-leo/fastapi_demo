from typing import *

import redis


def pass_through(cli: redis.Redis, class_: Any, redis_key: str, ex, callback: Callable,
                 args: List[Any]):
    d_exist = cli.exists(redis_key)
    if d_exist:
        data = cli.get(redis_key)
        if data is not None:
            return data
    # not fetch in cache
    data = callback(*args)
    cli.set(redis_key, data)
    return data


def logic_expire(cli, redis_key, callback):
    """
"""
    pass
