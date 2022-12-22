from app import create_app, db
from app.models.role import Role
from app.models.user import User

app = create_app('default')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, Role=Role)
