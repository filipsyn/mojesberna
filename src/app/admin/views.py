from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required


from ..models import User, Material, PriceList

admin = Blueprint('admin', __name__)


@admin.route('/users')
@login_required
def users_page():
    user_request = User.query.all()
    return render_template("admin/users.jinja2", title=f"Přehled uživatelů",
                           user_request=user_request)
