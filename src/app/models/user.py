from .. import db


class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64))
    telephone_number = db.Column(db.String(17))
    login = db.Column(db.String(128), nullable=False, unique=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.role_id'))

    permanent_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))
    temporary_residence_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'))

    permanent_residence = db.relationship("Address", foreign_keys=[permanent_residence_id])
    temporary_residence = db.relationship("Address", foreign_keys=[temporary_residence_id])

    def __repr__(self):
        return f"User: id:{self.user_id} - name:{self.first_name} {self.last_name} login: {self.login}"
