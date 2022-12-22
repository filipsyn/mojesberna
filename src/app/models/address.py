from .. import db


class Address(db.Model):
    __tablename__ = 'address'
    address_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(64))
    house_number = db.Column(db.String(16), nullable=False)
    zip_code = db.Column(db.String(16), nullable=False)

    def __repr__(self):
        return f"Address: id {self.address_id} - {self.house_number} {self.street}, {self.city}, {self.zip_code}"
