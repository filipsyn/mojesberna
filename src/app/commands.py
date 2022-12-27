from .models import Role, Status, User, Address, Material, PriceList, Purchase


def shell_context():
    return dict(Address=Address, Material=Material, PriceList=PriceList, Purchase=Purchase, Role=Role, Status=Status,
                User=User)
