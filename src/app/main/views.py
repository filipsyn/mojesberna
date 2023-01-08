from flask import Blueprint, render_template, flash
from flask_login import current_user

from .forms.EditPriceForm import EditPriceForm
from ..models import Material, PriceList

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    data = {
        'stats': {
            'Noviny': 1200,
            'Železo': 980,
            'Měď': 375,
            'Hliník': 525,
            'Olovo': 692,
        },
        'prices': {
            'Noviny': 2.70,
            'Železo': 4.50,
            'Měď': 85,
            'Mosaz': 45,
            'Olovo': 20
        }
    }
    return render_template('main/homepage.jinja2', title='Domovská stránka', data=data)


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
