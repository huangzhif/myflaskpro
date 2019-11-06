from flask import Blueprint,render_template

bp_users = Blueprint("bp_users",__name__,url_prefix="/users")


@bp_users.route("/users_list")
def users_list():
    return render_template("usersinfo/users_list.html")