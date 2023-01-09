from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms_sqlalchemy.fields import QuerySelectField

from ...models.material import Material


class EditPriceForm(FlaskForm):
    opts = QuerySelectField(query_factory=Material.get_query, allow_blank=False, get_label=lambda x: x.name)
    price = StringField('Cena (Kč)', validators=[DataRequired()])
    submit = SubmitField('Potvrdit')
