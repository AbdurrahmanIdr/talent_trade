from flask import Flask

from dotenv import load_dotenv

from app.extensions import db, migrate, mail, login_manager
from app.config import config

from app import models
from app import routes

from app.routes.main import main_bp as main
from app.routes.auth import auth_bp as auth
from app.routes.dashboard import dashboard_bp as dashboard
from app.routes.job import job_bp as job
from app.routes.application import application_bp as application
from app.routes.user import user_bp as user
from app.routes.review import bp as review
from app.routes.message import message_bp as message
from app.routes.payment import payment_bp as payment

from app.utils.helpers import truncate_words


def create_app(config_name='development'):
    app = Flask(__name__)
    load_dotenv()

    app.config.from_object(config[config_name])
    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()

    app.jinja_env.filters['truncate_words'] = truncate_words

    app.register_blueprint(main, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(dashboard, url_prefix='/dashboard')
    app.register_blueprint(job, url_prefix='/job')
    app.register_blueprint(application, url_prefix='/application')
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(review, url_prefix='/review')
    app.register_blueprint(message, url_prefix='/message')
    app.register_blueprint(payment, url_prefix='/payment')
    
    @login_manager.user_loader
    def load_user(user_id):
        return models.User.query.get(int(user_id))

    return app
