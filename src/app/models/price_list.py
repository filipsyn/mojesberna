from datetime import datetime

from .. import db


class PriceList(db.Model):
    __tablename__ = 'price_list'

    price_id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"Price id: {self.price_id} - {self.price} Kč on {self.date}"
