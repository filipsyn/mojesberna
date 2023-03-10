from enum import Enum

from .. import db


class UserStatus(Enum):
    WAITING = 'Čeká'
    ACTIVE = 'Aktivní'
    BANNED = 'Zablokovaný'


class Status(db.Model):
    __tablename__ = 'statuses'
    status_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    default = db.Column(db.Boolean, default=False)
    users = db.relationship('User', backref='status')

    def __init__(self, name: str, default: bool = False):
        self.name = name
        self.default = default

    def __repr__(self):
        return f"<Status ID {self.status_id}; {self.name}; (default {self.default})"

    @staticmethod
    def insert_statuses():
        statuses = [status.value for status in UserStatus]
        default_status = UserStatus.WAITING.value

        for s in statuses:
            status = Status.query.filter_by(name=s).first()
            if status is None:
                status = Status(s)
            status.default = (s == default_status)
            db.session.add(status)
        db.session.commit()
