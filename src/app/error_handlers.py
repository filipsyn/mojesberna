from flask import render_template


def error_page_not_found(e):
    return render_template('errors/404.jinja2', title='404')


def error_unauthorized(e):
    return render_template('errors/401.jinja2', title='401')


def error_forbidden(e):
    return render_template('errors/403.jinja2', title='403')


def error_internal_server_error(e):
    return render_template('errors/500.jinja2', title='500')
