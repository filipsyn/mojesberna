import click
from flask_migrate import upgrade

from .models import Role, Status, User, Address, Material, PriceList, Purchase, Permission


@click.command()
def prepare_database():
    # Applies database migrations
    upgrade()

    # Data seeding
    Role.insert_roles()
    Status.insert_statuses()


@click.command()
def seed_data():
    Material.seed_materials()


def shell_context():
    return dict(Address=Address, Material=Material, PriceList=PriceList, Purchase=Purchase, Role=Role, Status=Status,
                User=User, Permission=Permission)
