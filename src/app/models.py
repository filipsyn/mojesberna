from . import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    telephone_number = db.Column(db.String(17))
    password_hash = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f"User: id:{self.user_id} - name:{self.first_name} {self.last_name}"


class Role(db.Model):
    __tablename__ = 'roles'

    role_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)

    def __repr__(self):
        return f"Role {self.name}"
