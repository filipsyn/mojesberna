import click
from flask_migrate import upgrade

from .models import Role, Status, User, Address, Material, PriceList, Purchase


@click.command()
def prepare_database():
    # Applies database migrations
    upgrade()

    # Data seeding
    Role.insert_roles()
    Status.insert_statuses()


def shell_context():
    return dict(Address=Address, Material=Material, PriceList=PriceList, Purchase=Purchase, Role=Role, Status=Status,
                User=User)
