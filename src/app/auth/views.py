from flask import Blueprint

auth = Blueprint('auth', __name__)


@auth.route('/register')
def view_register_page():
    return "register page"
