from flask import Blueprint, render_template, flash, redirect, url_for

from .forms.EditPriceForm import EditPriceForm
from .. import db
from ..blueprints.stats.services.statistics import Statistics
from ..models import PriceList

main = Blueprint('main', __name__)


@main.route('/')
def view_home_page():
    price_query = Statistics.get_price_list()
    data = {
        'stats': {
            'Noviny': 1200,
            'Železo': 980,
            'Měď': 375,
            'Hliník': 525,
            'Olovo': 692,
        },
        'prices': price_query
    }
    return render_template('main/homepage.jinja2', title='Domovská stránka', data=data)


@main.route('/greet')
def view_greeting_page():
    return render_template('main/greet.jinja2', title='Greeting', greeting='Hello')


@main.route('/prices')
def add_material_prices():
    price_query = Statistics.get_price_list()

    return render_template('main/price_list.jinja2', title='Ceník', prices_request=price_query)


@main.route('/prices/edit', methods=['GET', 'POST'])
def edit_material_price():
    form = EditPriceForm()

    if form.validate_on_submit():
        new_price = PriceList(form.opts.data.material_id, form.price.data)
        db.session.add(new_price)
        db.session.commit()
        flash("Cena materiálu byla úspešně aktualizována", 'success')
        return redirect(url_for('main.add_material_prices'))
    return render_template("main/EditPriceList.jinja2", form=form)
