from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)


@auth.route('/register')
def view_register_page():
    return render_template('auth/register.jinja2', title='Registrace')
