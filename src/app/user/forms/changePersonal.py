from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Regexp, EqualTo, Length


class ChangePersonalForm(FlaskForm):
    first_name = StringField('Jméno', validators=[DataRequired()])
    last_name = StringField('Příjmení')
    telephone_number = StringField('Telefonní číslo', validators=[
        DataRequired(),
        Regexp(r'^(\+[0-9]{1,3})?( |-)?[0-9]{3}( |-)?[0-9]{3,4}( |-)?[0-9]{0,4}$')
    ])
    submit = SubmitField('Změnit')
