from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user

from .forms import RegisterForm, LoginForm
from .. import db
from ..models import User, Address

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
        address = Address(
            form.street.data,
            form.house_number.data,
            form.city.data,
            form.zip_code.data
        )
        new_user.permanent_residence = address
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('auth.view_login_page'))

    return render_template('auth/register.jinja2', title='Registrace', form=form)


@auth.route('/login', methods=['GET', 'POST'])
def view_login_page():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user is not None and user.verify_password(form.password.data):
            if user.is_banned():
                flash('Účet byl zablokován.')
                return redirect(url_for('main.view_home_page'))
            if user.is_waiting():
                flash('Potvrďte svou registraci na pobočce')
                return redirect(url_for('main.view_home_page'))
            login_user(user, form.remember_login.data)
            flash('Uživatel přihlášen')
        flash('Nesprávné přihlašovací jméno nebo heslo')
        return redirect(url_for('main.view_home_page'))
    return render_template('auth/login.jinja2', title='Příhlásit se', form=form)


@auth.route('/logout')
def logout():
    logout_user()
    flash('Odhlášení proběhlo úspěšně')
    return redirect(url_for('main.view_home_page'))
