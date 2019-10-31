import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from werkzeug.utils import import_string


basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# 导入蓝图名称
# from app.main.test import abc
blueprints = [
    "app.main.test:abc"
]


def create_app():
    app = Flask(__name__,instance_relative_config=True)

    app.config.from_object('config')
    app.config.from_pyfile("config.py")
    # app.register_blueprint(abc)
    register_logging(app)

    for bp_name in blueprints:
        bp = import_string(bp_name)
        app.register_blueprint(bp)

    return app


def register_logging(app):
    app.logger.setLevel(logging.INFO)
    formatter = logging.Formatter("[%(asctime)s]-[%(filename)s]-[%(levelname)s]-[%(funcName)s]-[%(lineno)s]-%(message)s")
    file_handler = RotatingFileHandler(os.path.join(basedir,"logs/myflaskpro.log"),
                                       maxBytes=10*1024*1024,backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    if not app.debug:
        app.logger.addHandler(file_handler)