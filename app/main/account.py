from flask import Blueprint, current_app, render_template

bp_login = Blueprint("bp_login", __name__, url_prefix="/account")


@bp_login.route("/login")
def login():
    return render_template("account/login.html")
