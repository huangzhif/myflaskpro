from flask import current_app,Blueprint,render_template

# 蓝图名字不能与视图名相同
bp_index = Blueprint('bp_index',__name__)


@bp_index.route("/")
@bp_index.route("/index")
def index():
    current_app.logger.info("index")
    return render_template("base.html")