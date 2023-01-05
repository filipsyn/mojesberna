from .. import db


class Material(db.Model):
    __tablename__ = 'materials'

    material_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False, unique=True)
    purchases = db.relationship('Purchase', backref='material')
    prices = db.relationship('PriceList', backref='material')

    def __repr__(self):
        return f"Material id: {self.material_id} - {self.name}"

    def __init__(self, name):
        self.name = name

    @staticmethod
    def seed_materials():
        materials = ['Letákový papír', 'Železo', 'Měď', 'Mosaz', 'Olovo', 'Hliník', 'Směsný papír', 'Kartón',
                     'Autobaterie']

        for m in materials:
            material = Material.query.filter_by(name=m).first()
            if material is None:
                material = Material(m)
            db.session.add(material)
        db.session.commit()
