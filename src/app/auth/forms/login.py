from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    login = StringField('', validators=[DataRequired()])
    password = PasswordField('', validators=[DataRequired()])
    remember_login = BooleanField('')
