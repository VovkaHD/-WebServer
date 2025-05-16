import datetime
import sqlalchemy
from flask_login import UserMixin
from sqlalchemy import orm

from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    email = sqlalchemy.Column(sqlalchemy.VARCHAR, index=True, unique=True, nullable=True)
    hashed_password = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    admin = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)

    def __repr__(self):
        return f'{self.id} {self.email} {self.admin}'

    def set_password(self, password):
        self.hashed_password = password

    def check_password(self, password):
        if self.hashed_password == password:
            return True
