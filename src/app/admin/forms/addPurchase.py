from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ...models.material import Material
from ...models.user import User


class AddPurchaseForm(FlaskForm):
    weight = StringField('hmotnost', validators=[DataRequired()])
    description = StringField('popis', validators=[DataRequired()])
    material_id = QuerySelectField('materiál', query_factory=Material.get_query, allow_blank=False, get_label=lambda x: x.name)
    selling_customer_id = QuerySelectField('prodávající', query_factory=User.get_query, allow_blank=False, get_label=lambda x: x.login)
    submit = SubmitField('Přidat výkup')
