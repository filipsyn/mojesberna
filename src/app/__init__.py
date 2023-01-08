from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy

from .config import config

# Creating objects for external applications
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
moment = Moment()


def create_app(config_name='default') -> Flask:
    """Factory function for creating application instances

    This function creates new instance of flask application. Then it initializes external packages,
    loads in blueprints and returns constructed app instance.

    :returns:
        An instance of flask application
    """
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    # Initialization of external packages
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    moment.init_app(app)

    # Preparation of subcommands for `flask` command. eg. flask shell, flask seed-data` flask prepare-database
    from .commands import prepare_database, shell_context, seed_data
    app.cli.add_command(prepare_database)
    app.cli.add_command(seed_data)
    app.shell_context_processor(shell_context)

    # Import and register error handlers
    from .error_handlers import error_forbidden, error_unauthorized, error_page_not_found, error_internal_server_error
    app.register_error_handler(401, error_unauthorized)
    app.register_error_handler(403, error_forbidden)
    app.register_error_handler(404, error_page_not_found)
    app.register_error_handler(500, error_internal_server_error)

    # Importing blueprints
    from .main.views import main as main_blueprint
    app.register_blueprint(main_blueprint)
    from .auth.views import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix="/auth/")
    from .user.views import user as user_blueprint
    app.register_blueprint(user_blueprint, url_prefix="/user/")
    from .admin.views import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix="/admin/")

    return app
