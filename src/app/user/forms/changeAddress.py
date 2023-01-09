from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo, Length


class ChangeAddressForm(FlaskForm):
    street = StringField('Ulice')
    house_number = StringField('Číslo popisné', validators=[DataRequired()])
    city = StringField('Město/Obec', validators=[DataRequired()])
    zip_code = StringField('PSČ', validators=[DataRequired(), Length(min=5, message="PSČ musí mít alespoň 5 čísel")])

    submit = SubmitField('Přidat uživatele')
