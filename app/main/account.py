from app.forms.account import LoginForm
from flask import Blueprint, current_app, redirect, render_template, request, url_for
from flask_login import current_user,login_user

bp_account = Blueprint("bp_account", __name__, url_prefix="/account")


@bp_account.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('bp_index.index'))
    return render_template("account/login.html", form=form)


@bp_account.route("/logout")
def logout():
    print("abc")
    return redirect(url_for(".login"))
