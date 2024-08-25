from flask import Flask

from app.extensions import db, migrate
from app.config import config

from app import models
# from app import routes

from app.routes.main import main_bp as main
from app.routes.auth import auth_bp as auth


def create_app(config_name='development'):
    app = Flask(__name__)

    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        db.create_all()

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
