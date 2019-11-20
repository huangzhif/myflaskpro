import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask,session
from werkzeug.utils import import_string
# from flask_bootstrap import Bootstrap
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate
# from flask_login import LoginManager
from datetime import datetime,timedelta
from app.models import User,Games,Channels,Zones,Membership
from app.extensions import bootstrap,db,migrate,login_manager,csrf


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app():
    app = Flask(__name__,instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile("config.py")
    # app.config.from_envvar("APP_CONFIG_FILE")

    # 注册扩展
    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    # register_modelobj()
    register_shell_context(app)
    register_session_lifetime(app)

    return app


def register_session_lifetime(app):
    @app.before_request
    def before_request():
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=30)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User,
                    Games=Games, Channels=Channels, Zones=Zones,Membership=Membership)


def register_blueprint(app):
    # from app.main.test import abc
    blueprints = [
        "app.main.test:abc",
        "app.main.index:bp_index",
        "app.main.account:bp_account",
        "app.main.usersinfo:bp_users",
        "app.main.game:bp_game"
    ]
    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)


def register_extensions(app):
    """
    第三方扩展
    :param app:
    :return:
    """
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app,db)
    login_manager.init_app(app)
    csrf.init_app(app)


def register_logging(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)s]-%(message)s")
    file_handler = RotatingFileHandler(os.path.join(basedir,"logs/myflaskpro.log"),
                                       maxBytes=10*1024*1024,backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # if not app.debug:
    app.logger.addHandler(file_handler)



