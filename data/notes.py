import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
import sqlalchemy.ext.declarative as dec


class Notes(SqlAlchemyBase):
    __tablename__ = 'notes'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    team_leader = sqlalchemy.Column(sqlalchemy.Integer,
                                    sqlalchemy.ForeignKey("users.id"))
    note = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    note_time = sqlalchemy.Column(sqlalchemy.Time, nullable=True)
    email_send = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    description = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    start_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    end_date = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    is_finished = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    user = orm.relationship('User')

    def __repr__(self):
        return f"<Note> {self.id} {self.note} {self.collaborators}"
