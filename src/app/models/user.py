from enum import Enum

from flask_login import UserMixin

from .. import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class UserStatus(Enum):
    WAITING = 'Waiting'
    ACTIVE = 'Active'
    BANNED = 'banned'


class User(db.Model, UserMixin):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    telephone_number = db.Column(db.String(17))
    login = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))
    status = db.Column(db.Enum(UserStatus), default=UserStatus.WAITING)

    permanent_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    temporary_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))

    permanent_residence = db.relationship("Address", foreign_keys=[permanent_residence_id])
    temporary_residence = db.relationship("Address", foreign_keys=[temporary_residence_id])

    def __init__(self, first_name: str, last_name: str, telephone: str, login: str, password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.telephone_number = telephone
        self.login = login
        self.password_hash = password
        self.status = UserStatus.WAITING

    def confirm(self):
        if self.status is UserStatus.WAITING:
            self.status = UserStatus.ACTIVE

    def ban(self):
        if self.status is UserStatus.ACTIVE:
            self.status = UserStatus.BANNED

    def unban(self):
        if self.status is UserStatus.BANNED:
            self.status = UserStatus.ACTIVE

    def __repr__(self):
        return f"<User ID:{self.user_id}; Full name:{self.first_name} {self.last_name}; login: {self.login}, " \
               f"Status: {self.status.value}>"
