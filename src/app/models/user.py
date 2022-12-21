from .. import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    telephone_number = db.Column(db.String(17))
    password_hash = db.Column(db.String(128), nullable=False)
