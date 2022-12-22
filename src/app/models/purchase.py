from datetime import datetime

from .. import db


class Purchase(db.Model):
    __tablename__ = 'purchases'

    purchase_id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    description = db.Column(db.Text)
    buying_employee_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    selling_customer_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    material_id = db.Column(db.Integer, db.ForeignKey('materials.material_id'))

    def __repr__(self):
        return f"Purchase id: {self.purchase_id} - {self.weight} kg on {self.date}"
