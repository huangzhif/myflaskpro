import json
from app.models import db, User
# from app.models import User
from flask import Blueprint,render_template,flash,request,jsonify
from app.forms.usersinfo import CreateUserForm
from app.apis.api import PyCrypt


bp_users = Blueprint("bp_users",__name__,url_prefix="/users")


@bp_users.route("/users_list")
def users_list():
    users = User.query.order_by("username")
    return render_template("usersinfo/users_list.html",users=users)


@bp_users.route("/get_users")
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
def create_user():
    form = CreateUserForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,email=form.email.data,is_active=form.is_active.data)
        password = PyCrypt.gen_rand_pass(16)
        # password = "123456"
        # print(password)
        user.set_password(password)
        db.session.add(user)
        try:
            db.session.commit()
            flash("Succeed","alert-info")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash("fail","alert-danger")

    return render_template("usersinfo/create_user.html", form=form)
