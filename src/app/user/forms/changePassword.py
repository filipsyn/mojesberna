from flask_wtf import FlaskForm
from wtforms import SubmitField, PasswordField
from wtforms.validators import DataRequired, EqualTo


class ChangePasswordform(FlaskForm):
    password = PasswordField('Heslo', validators=[DataRequired()])
    confirm_password = PasswordField('Potvrďte heslo', validators=[DataRequired(), EqualTo('password')])

    submit = SubmitField('Změnit heslo')
