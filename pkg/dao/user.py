from typing import *

from pkg import constant
from pkg.codes.code import *
from pkg.dao.db import session_scope
from pkg.model.user import User
from pkg.schemas.user import *
from pkg.utils.snow_flake import get_snow_id


# CRUD

def create_user(info: RequestRegister) -> Union[User, None]:
    u = None
    with session_scope() as session:
        n_u = User(uuid=get_snow_id(), username=info.username)
        n_u.password = info.password
        session.add(n_u)
        session.commit()
        if n_u is not None:
            u = User(**n_u.to_dict())
    return u if u and u.id != 0 else None


def fetch_user(user_id: int = 0, username="") -> User:
    u = None
    with session_scope() as session:
        if user_id:
            u = session.query(User).filter(User.uuid == user_id).first()
        elif username:
            u = session.query(User).filter(User.username == username).first()
        else:
            raise Exception(REQUEST_PARAM_ERROR)
        if u is not None:
            u = User(**u.to_dict())
    return u


def fetch_users(user_ids) -> List[User]:
    users = []
    with session_scope() as session:
        users = session.query(User).filter(User.uuid.in_(user_ids)).all()
        if users is None:
            users = []
        users = [User(**x.to_dict()) for x in users]
    return users


def update_user(uuid: int, u: Dict[str, Any]) -> bool:
    res = False
    if uuid is None:
        return res
    # can't update column
    for ch in constant.user.UserNoUpdateColumn:
        u.pop(ch) if ch in u else None
    if len(u.keys()) <= 0:
        return True
    with session_scope() as session:
        session.query(User).filter(User.uuid == uuid).update(u)
    return res


def delete_user(info):
    pass
