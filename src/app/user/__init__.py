from ..models import Material


def get_user_attributes(user):
    user_attributes = {

    }
    return user_attributes


def get_price_list():
    material = Material.query.all()

    return material
