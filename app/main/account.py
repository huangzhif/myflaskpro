from flask import Blueprint, current_app, render_template
from app.forms.account import LoginForm

bp_login = Blueprint("bp_login", __name__, url_prefix="/account")


@bp_login.route("/login")
def login():
    form = LoginForm()
    return render_template("account/login.html", form=form)
