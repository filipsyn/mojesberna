from flask import Flask


# Creating objects for external applications
# db = SQLAlchemy()


def create_app() -> Flask:
    """Factory function for creating application instances

    This function creates new instance of flask application. Then it initializes external packages,
    loads in blueprints and returns constructed app instance.

    :returns:
        A instance of flask application
    """
    app = Flask(__name__)

    # Initialization of external packages
    # db.init_app(app)

    # Importing blueprints
    from .blueprints.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
