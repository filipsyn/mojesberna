from flask import Blueprint, render_template

from .forms import RegisterForm
from .. import db
from ..models import User

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def view_register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(
            form.first_name.data,
            form.last_name.data,
            form.telephone_number.data,
            form.login.data,
            form.password.data
        )
        db.session.add(new_user)
        db.session.commit()

    return render_template('auth/register.jinja2', title='Registrace', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def view_login_page():
    pass
