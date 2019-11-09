from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,HiddenField
from wtforms.validators import DataRequired, Email


class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    is_active = BooleanField("Is_Active")
    submit = SubmitField("Submit")


class EditUserForm(FlaskForm):
    id = HiddenField("id")
    username = StringField("Username", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    is_active = BooleanField("Is_Active")
    submit = SubmitField("Submit")
