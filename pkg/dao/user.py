from pkg.dao.mysql import get_db
from pkg.model.user import User
from pkg.request.user import *
from pkg.codes.code import *
from typing import *


# CRUD

def CreateUser(info: RequestRegister):
    db = get_db()
    u = User(username=info.username)
    u.password = info.password
    db.add(u)
    db.commit()


def FetchUser(user_id: int, username="") -> Dict:
    db = get_db()
    res = None
    if user_id:
        res = db.query(User).filter(User.uuid == user_id).one()
    elif username:
        res = db.query(User).filter(User.username == username).one()
    else:
        raise Exception(REQUEST_PARAM_ERROR)

    return res.to_dict()


def FetchUsers(user_ids):
    db = get_db()


def UpdateUser(info):
    db = get_db()


def DeleteUser(info):
    db = get_db()
