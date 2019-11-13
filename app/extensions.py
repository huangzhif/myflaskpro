from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect


bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "bp_account.login"
login_manager.login_message_category = "alert-warning"
login_manager.login_message = "Access denied"
login_manager.session_protection = "strong"
csrf = CSRFProtect()