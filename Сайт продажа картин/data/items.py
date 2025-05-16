import sqlalchemy

from data.db_session import SqlAlchemyBase


class i_item(SqlAlchemyBase):
    __tablename__ = 'items'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.VARCHAR, unique=True)
    more = sqlalchemy.Column(sqlalchemy.VARCHAR, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.VARCHAR)
    image = sqlalchemy.Column(sqlalchemy.VARCHAR, unique=True)
    link = sqlalchemy.Column(sqlalchemy.VARCHAR, unique=True)

    def __repr__(self):
        return f'{self.id}&{self.name}&{self.more}&{self.price}&{self.image}&{self.link}'
