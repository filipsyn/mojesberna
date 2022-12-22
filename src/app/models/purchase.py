from .. import db
from datetime import datetime


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
