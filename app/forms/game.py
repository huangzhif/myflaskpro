from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,HiddenField
from wtforms.validators import DataRequired


class CreateGameForm(FlaskForm):
    game = StringField("游戏", validators=[DataRequired()])
    local_initshell_path = StringField("本地初始化脚本路径",
                                       validators=[DataRequired()],
                                       render_kw={"placeholder": "本地初始化路径",
                                                  "id": "id_local_initshell_path",
                                                  "class": "form-control"})
    remote_initshell_path = StringField("远端初始化脚本路径",
                                        validators=[DataRequired()],
                                        render_kw={'placeholder': "远端初始化路径",
                                                   "id": "id_remote_initshell_path",
                                                   "class": "form-control"})

    submit = SubmitField("Submit")


class EditGameForm(FlaskForm):
    id = HiddenField("id")
    game = StringField("游戏", validators=[DataRequired()])
    local_initshell_path = StringField("本地初始化脚本路径",
                                       validators=[DataRequired()],
                                       render_kw={"placeholder": "本地初始化路径",
                                                  "id": "id_local_initshell_path",
                                                  "class": "form-control"})
    remote_initshell_path = StringField("远端初始化脚本路径",
                                        validators=[DataRequired()],
                                        render_kw={'placeholder': "远端初始化路径",
                                                   "id": "id_remote_initshell_path",
                                                   "class": "form-control"})

    submit = SubmitField("Submit")
