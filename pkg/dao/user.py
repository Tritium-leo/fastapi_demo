from pkg.dao.mysql import session_scope, Session
from pkg.model.user import User
from pkg.codes.code import *
from pkg.schemas.user import *
from typing import *
from pkg.utils.snow_flake import get_snow_id


# CRUD

def create_user(info: RequestRegister) -> Union[Dict, None]:
    u = None
    with session_scope() as session:
        u = User(uuid=get_snow_id(), username=info.username)
        u.password = info.password
        session.add(u)
        session.commit()
        u = u.to_dict()
    return u if u["id"] != 0 else None


def fetch_user(user_id: int = 0, username="") -> Dict:
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


def fetch_users(user_ids) -> List[Dict]:
    users = []
    with session_scope() as session:
        users = session.query(User).filter(User.uuid.in_(user_ids)).all()
        if users is None:
            users = []
        users = [x.to_dict() for x in users]
    return users


def update_user(info):
    pass


def delete_user(info):
    pass
