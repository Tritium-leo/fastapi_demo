from . import Base
from sqlalchemy import Column, Integer, String, BIGINT, Table, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash
from pkg.model.constant import *
from pydantic import BaseModel

role_user = Table("role_user",
                  Base.metadata,
                  Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
                  Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
                  )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 4640214741665447937
    uuid = Column(BIGINT, nullable=False)
    username = Column(String(20), nullable=False)
    _password_hash_ = Column(String(256), nullable=False)

    # 多对多关联
    roles = relationship('Role', secondary=role_user, backref=backref('users', lazy='dynamic'))

    @property
    def password(self):
        return Exception("password can't be get")

    @password.setter
    def password(self, value):
        self._password_hash_ = generate_password_hash(value)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self._password_hash_, password)

    @classmethod
    def check_username(cls, username: str) -> bool:
        if len(username) < UserNameMinLen or len(username) >= UsernameMaxLen:
            return False
        return True
