from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    return render_template('main/homepage.jinja2', title='Domovská stránka')


@main.route('/greet')
def view_greeting_page():
    return render_template('main/greet.jinja2', title='Greeting', greeting='Hello')
