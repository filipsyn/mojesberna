from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class UpdatePriceListForm(FlaskForm):
    price = StringField('Cena', validators=[DataRequired()])

    submit = SubmitField('Upravit')
