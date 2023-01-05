from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import Role, Status, UserStatus
from .. import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    telephone_number = db.Column(db.String(17))
    login = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    status_id = db.Column(db.Integer, db.ForeignKey('statuses.status_id'))

    permanent_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    temporary_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))

    permanent_residence = db.relationship("Address", foreign_keys=[permanent_residence_id])
    temporary_residence = db.relationship("Address", foreign_keys=[temporary_residence_id])

    def __init__(self, first_name: str, last_name: str, telephone: str, login: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.telephone_number = telephone
        self.login = login
        self.password_hash = generate_password_hash(password)

        if self.status is None:
            self.status = Status.query.filter_by(default=True).first()

        if self.role is None:
            self.role = Role.query.filter_by(default=True).first()

    def get_id(self):
        return self.user_id

    def is_waiting(self):
        return self.status.name == UserStatus.WAITING.value

    def confirm(self):
        if self.status.name == UserStatus.WAITING.value:
            self.status = Status.query.filter_by(name=UserStatus.ACTIVE.value).first()

    def is_active(self):
        return self.status.name == UserStatus.ACTIVE.value

    def ban(self):
        if self.status.name == UserStatus.ACTIVE.value:
            self.status = Status.query.filter_by(name=UserStatus.BANNED.value).first()

    def is_banned(self):
        return self.status.name == UserStatus.BANNED.value

    def unban(self):
        if self.status.name == UserStatus.BANNED.value:
            self.status = Status.query.filter_by(name=UserStatus.ACTIVE.value).first()

    def can(self, perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_worker(self):
        return self.role.name == 'Worker'

    def is_administrator(self):
        return self.role.name == 'Administrator'

    @staticmethod
    def get_query():
        return User.query

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User ID:{self.user_id}; Full name:{self.first_name} {self.last_name}; login: {self.login}, " \
               f"Status: {self.status.name}>"
