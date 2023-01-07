from flask import Blueprint, render_template, request, flash
from forms import EditPriceForm
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


@main.route('/prices/edit', methods=['GET', 'POST'])
def edit_material_price():

    form = EditPriceForm()
    price_to_update = PriceList.query.get_or_404(id)
    if request.method == "POST":
        price_to_update.price = request.form['price']
        try:
            db.session.commit()
            flash('Změna ceny proběhla úspěšně')
            return render_template("main/EditPriceList.jinja2", form=form, price_to_update=price_to_update)
        except:
            flash('Error')
            return render_template("main/EditPriceList.jinja2", form=form, price_to_update=price_to_update)
    else:
        return render_template("main/EditPriceList.jinja2", form=form, price_to_update=price_to_update)
