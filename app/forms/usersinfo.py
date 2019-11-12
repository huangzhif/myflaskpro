from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,HiddenField
from wtforms.validators import DataRequired, Email


class AEUserForm(FlaskForm):
    id = HiddenField("id")
    username = StringField("用户名", validators=[DataRequired()])
    email = StringField("邮箱", validators=[DataRequired(), Email()])
    is_active = BooleanField("是否启用")
    submit = SubmitField("Submit")
