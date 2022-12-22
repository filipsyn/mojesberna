import os

from dotenv import load_dotenv

dotenv_path = os.path.join('..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Config:
    SECRET_KEY = os.environ.get('MOJESBERNA_SECRET_KEY')

    @staticmethod
    def get_connection_string():
        user = os.environ.get('POSTGRES_USER') or 'postgres'
        password = os.environ.get('POSTGRES_PASSWORD') or 'keyboard-cat'
        db_name = os.environ.get('POSTGRES_DB') or 'sberna-db'
        host = os.environ.get('POSTGRES_HOST') or 'localhost'
        port = os.environ.get('POSTGRES_PORT') or 5432

        return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"

    SQLALCHEMY_DATABASE_URI = get_connection_string()

    @staticmethod
    def init_app(app):
        pass


config = {
    'default': Config
}
