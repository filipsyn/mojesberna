from flask import Blueprint, render_template

from .. import db
from ..models import Material, PriceList
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

    return render_template('main/price_list.jinja2', title='Ceník', prices_request=prices_request)


