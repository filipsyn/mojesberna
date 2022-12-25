from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('Přihlašovací jméno', validators=[DataRequired()])
    password = PasswordField('Heslo', validators=[DataRequired()])
    remember_login = BooleanField('Zůstat přilášený')
