from flask import current_app,Blueprint,render_template

# 蓝图名字不能与模块名（即文件名）相同
abc = Blueprint('abc',__name__)


@abc.route("/")
@abc.route("/test")
def test():
    current_app.logger.info("test log.")
    return render_template("base.html")