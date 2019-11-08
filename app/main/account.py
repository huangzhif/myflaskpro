from app.forms.account import LoginForm
from flask import Blueprint, current_app, redirect, render_template, request, url_for,flash,abort
from flask_login import current_user,login_user,logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse
from is_safe_url import is_safe_url

bp_account = Blueprint("bp_account", __name__, url_prefix="/account")


@bp_account.route("/login", methods=["GET", "POST"])
def login():
    """
    用户登录
    :return:
    """
    if current_user.is_authenticated:
        return redirect(url_for('bp_index.index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password","alert-warning")
            return redirect(url_for('.login'))
        
        login_user(user, remember=form.remember_me.data)

        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('bp_index.index')

        # 后面allowhost按实际填写
        elif not is_safe_url(next_page,{"http://192.168.56.100:5000/"}):
            return abort(404)
        return redirect(next_page)
    return render_template("account/login.html", form=form)


@bp_account.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".login"))
