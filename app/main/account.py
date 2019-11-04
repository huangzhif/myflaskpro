from app.forms.account import LoginForm
from flask import Blueprint, current_app, redirect, render_template, request, url_for

bp_login = Blueprint("bp_login", __name__, url_prefix="/account")


@bp_login.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect(url_for('bp_index.index'))
    return render_template("account/login.html", form=form)
