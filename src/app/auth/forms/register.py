from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo, Length, ValidationError

from ...models import User


class RegisterForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired()])
    last_name = StringField('Příjmení')
    username = StringField('Přihlašovací jméno', validators=[
        DataRequired(),
        Length(min=3, max=128, message='Uživatelské jméno může mít délku 3-128 znaků')
    ])
    telephone_number = StringField('Telefonní číslo', validators=[
        DataRequired(),
        Regexp(r'^(\+[0-9]{1,3})?( |-)?[0-9]{3}( |-)?[0-9]{3,4}( |-)?[0-9]{0,4}$')
    ])
    password = PasswordField('Heslo', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrďte heslo', validators=[DataRequired(), EqualTo('password')])
    street = StringField('Ulice')
    house_number = StringField('Číslo popisné', validators=[DataRequired()])
    city = StringField('Město/Obec', validators=[DataRequired()])
    zip_code = StringField('PSČ', validators=[DataRequired(), Length(min=5, message="PSČ musí mít alespoň 5 čísel")])

    submit = SubmitField('Registrovat se')

    def validate_username(self, form):
        user = User.query.filter_by(login=form.data).first()
        if user:
            raise ValidationError("Uživatelské jméno je zabrané")
