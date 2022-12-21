from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Creating objects for external applications
db = SQLAlchemy()


def create_app() -> Flask:
    """Factory function for creating application instances

    This function creates new instance of flask application. Then it initializes external packages,
    loads in blueprints and returns constructed app instance.

    :returns:
        A instance of flask application
    """
    app = Flask(__name__)

    app.config.from_prefixed_env(prefix="MOJESBERNA")

    # Initialization of external packages
    db.init_app(app)

    # Importing blueprints
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
