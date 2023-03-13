from flask import Flask
from app.config import Config
from app.extensions import db, migrate, mail, jwt
from app.commands import init_db, populate_db
from app.api import api
from app.models.user import User



COMMANDS = [init_db, populate_db]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    register_extensions(app)
    register_commands(app)

    return app


def register_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    api.init_app(app)
    jwt.init_app(app)


def register_commands(app):
    for command in COMMANDS:
        app.cli.add_command(command)