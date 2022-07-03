from sqlalchemy import Column, Integer, String, BIGINT, Table, ForeignKey, SmallInteger
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from pkg import constant
from . import Base

role_user = Table("role_user",
                  Base.metadata,
                  Column("role_id", Integer, ForeignKey("roles.id"), primary_key=True),
                  Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
                  )


class UserState():
    cancel = -1  # 自己注销
    ban = 0  # 系统封
    normal = 1  # 正常


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # 4640214741665447937
    uuid = Column(BIGINT, nullable=False, unique=True)
    username = Column(String(20), nullable=False, unique=True)
    _password_hash_ = Column(String(256), nullable=False)
    state = Column(SmallInteger, nullable=False, default=UserState.normal)

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
        if len(username) < constant.user.UserNameMinLen or len(username) >= constant.user.UsernameMaxLen:
            return False
        return True

    # 账户是否是正常状态
    def is_normal(self) -> bool:
        return self.state == UserState.normal
