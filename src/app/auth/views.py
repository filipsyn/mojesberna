from flask import Blueprint, render_template

from .forms import RegisterForm

auth = Blueprint('auth', __name__)


@auth.route('/register', methods=['GET', 'POST'])
def view_register_page():
    form = RegisterForm()

    if form.validate_on_submit():
        pass
    return render_template('auth/register.jinja2', title='Registrace', form=form)
