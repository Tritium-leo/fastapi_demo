import datetime
import time
import typing
import uuid

import jwt

headers = {'alg': "HS256"}
# TODO TO CONFIG
securt_key = "whoisyourdaddy"


def get_token(payload: dict, px: int = -1):
    """:param px 过期时间"""
    salt = str(uuid.uuid4())[:5]
    if px > 0:
        px = min(px, 10 * 3600 * 1000)
        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(milliseconds=px)

    return salt + jwt.encode(payload, securt_key, algorithm="HS256", headers=headers)


def check_token(token: str) -> typing.Union[dict, None]:
    try:
        token = token[5:]
        return jwt.decode(token, securt_key, algorithms=["HS256"])
    except:
        return None


if __name__ == "__main__":
    payload = {"user": "chi", "uuid": 123}
    token = get_token(payload, 1000)
    time.sleep(1)
    check_payload = check_token(token)
    print(payload)
    print(token)
    print(check_payload)
