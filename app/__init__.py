import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from werkzeug.utils import import_string
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 导入蓝图名称
# from app.main.test import abc
blueprints = [
    "app.main.test:abc",
    "app.main.index:bp_index",
    "app.main.account:bp_account",
    "app.main.usersinfo:bp_users"
]

# 扩展
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__,instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile("config.py")

    # 注册扩展
    register_logging(app)
    register_extensions(app)
    register_blueprint(app)
    register_modelobj()
    register_shell_context(app)

    return app


def register_modelobj():
    # 在migrate之前需要导入 models
    from .models import User


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db, User=User)


def register_blueprint(app):
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


def register_logging(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)s]-%(message)s")
    file_handler = RotatingFileHandler(os.path.join(basedir,"logs/myflaskpro.log"),
                                       maxBytes=10*1024*1024,backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)



