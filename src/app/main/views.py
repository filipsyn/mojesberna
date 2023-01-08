from flask import Blueprint, render_template, flash, request, url_for
from .forms.EditPriceForm import EditPriceForm
from .. import db
from flask_login import current_user
from ..models import Material, PriceList, User

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    return render_template('main/homepage.jinja2', title='Domovská stránka')


@main.route('/greet')
def view_greeting_page():
    return render_template('main/greet.jinja2', title='Greeting', greeting='Hello')


@main.route('/prices')
def add_material_prices():
    prices_request = Material.query.join(PriceList, PriceList.material_id == Material.material_id).add_columns(
                                                                                                Material.name,
                                                                                                PriceList.price).all()
    user = current_user

    return render_template('main/price_list.jinja2', title='Ceník', prices_request=prices_request, user=user)


@main.route('/prices/edit', methods=['GET', 'POST'])
def edit_material_price():

    form = EditPriceForm()
    if form.validate_on_submit():
        flash(form.opts.data.material_id)
    return render_template("main/EditPriceList.jinja2", form=form)
