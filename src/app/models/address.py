from .. import db


class Address(db.Model):
    __tablename__ = 'addresses'
    address_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(64), nullable=False)
    street = db.Column(db.String(64))
    house_number = db.Column(db.String(16), nullable=False)
    zip_code = db.Column(db.String(16), nullable=False)

    def __init__(self, street, house_number, city, zip_code):
        self.city = city
        self.street = street
        self.house_number = house_number
        self.zip_code = zip_code

    def __repr__(self):
        return f"Address: id {self.address_id} - {self.house_number} {self.street}, {self.city}, {self.zip_code}"
