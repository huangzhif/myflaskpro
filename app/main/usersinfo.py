import json,time

from app.apis.api import PyCrypt
from app.forms.usersinfo import AEUserForm
from app.models import User, db
# from app.models import User
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required

bp_users = Blueprint("bp_users",__name__,url_prefix="/users")


@bp_users.route("/users_list")
@login_required
def users_list():
    # users = User.query.order_by("username")
    return render_template("usersinfo/users_list.html")


@bp_users.route("/get_users")
@login_required
def get_users():
    _table = []
    users = User.query.order_by("username")
    for idx, user in enumerate(users, 1):
        tmp = {}
        tmp['idx'] = idx
        tmp["username"] = user.username
        tmp["email"] = user.email
        _table.append(tmp)

    return jsonify(_table)


@bp_users.route("/create_user", methods=["GET", "POST"])
@login_required
def create_user():
    form = AEUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,is_active=form.is_active.data)
        password = PyCrypt.gen_rand_pass(16)
        # password = "123456"
        # print(password)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
            flash("添加成功", "alert-info")
            return redirect(url_for('.users_list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(e,"alert-danger")

    return render_template("createdit_module.html", form=form,title="新增用户")


@bp_users.route("/del_user", methods=["POST"])
@login_required
def del_user():
    username = request.form.get("username", "")
    user = User.query.filter_by(username=username).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        e = True
    return jsonify({"e": e, "msg": "succeed"})


@bp_users.route("/edit_user/<username>",methods=["GET","POST"])
@login_required
def edit_user(username):
    user = User.query.filter_by(username=username).first()
    form = AEUserForm(id=user.id,username=user.username,email=user.email,is_active=user.is_active)

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_active = form.is_active.data
        try:
            db.session.commit()
            flash("修改成功", "alert-info")
            return redirect(url_for('.users_list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(e, "alert-danger")

    return render_template("createdit_module.html",form=form,title="编辑用户")
