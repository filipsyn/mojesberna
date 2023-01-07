from flask import Blueprint, render_template

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    data = {
        'Noviny': 1200,
        'Železo': 980,
        'Měď': 375,
        'Hliník': 525
    }
    return render_template('main/homepage.jinja2', title='Domovská stránka', data=data)


@main.route('/greet')
def view_greeting_page():
    return render_template('main/greet.jinja2', title='Greeting', greeting='Hello')
