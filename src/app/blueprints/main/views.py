from . import main


@main.route('/')
def view_home_page():
    return "<h1>Hello world</h1>"
