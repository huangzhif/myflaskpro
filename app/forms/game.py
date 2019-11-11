from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,HiddenField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Optional
from app.models import Games,Channels


class AEGameForm(FlaskForm):
    id = HiddenField("id", validators=[Optional()])
    name = StringField("游戏", validators=[DataRequired()],
                       render_kw={
                           "id": "id_name",
                           "class": "form-control"
                       })
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

    submit = SubmitField("Submit",render_kw={"class":"btn btn-info btn-md"})


class AEChannelForm(FlaskForm):
    """
    新增/编辑 channel 表单
    """
    id = HiddenField("id", validators=[Optional()])
    name = StringField("渠道", validators=[DataRequired()],
                       render_kw={"id": "id_name", "class": "form-control"})

    remark = TextAreaField("备注", render_kw={"id": "id_remark",
                                            "class": "form-control"})

    submit = SubmitField("Submit",render_kw={"class":"btn btn-info btn-md"})


class AEZoneForm(FlaskForm):
    """
    新增/编辑 zone 表单
    """
    id = HiddenField("id", validators=[Optional()])
    game = SelectField("游戏", coerce=int,
                       render_kw={"id": "id_game", "class": "form-control"})
    channel = SelectField("渠道", coerce=int, render_kw={"id": "id_channel",
                                                       "class": "form-control"})

    zonenum = StringField("区服号", validators=[DataRequired()],
                          render_kw={"id": "id_zonenum",
                                     "class": "form-control"})
    zonename = StringField("区服名", validators=[DataRequired()],
                           render_kw={"id": "id_zonename",
                                      "class": "form-control"})
    zoneip = StringField("区服IP", validators=[DataRequired()],
                         render_kw={"id": "id_zoneip",
                                    "class": "form-control"})
    dblink = StringField("数据库链接", validators=[DataRequired()],
                         render_kw={"id": "id_dblink",
                                    "class": "form-control"})
    dbport = StringField("数据库端口", validators=[DataRequired()],
                         render_kw={"id": "id_dbport",
                                    "class": "form-control"})
    db_A = StringField("数据库A", validators=[DataRequired()],
                       render_kw={"id": "id_ddb_A", "class": "form-control"})
    db_B = StringField("数据库B", validators=[DataRequired()],
                       render_kw={"id": "id_ddb_B", "class": "form-control"})
    db_C = StringField("数据库C", validators=[DataRequired()],
                       render_kw={"id": "id_ddb_C", "class": "form-control"})

    submit = SubmitField("Submit", render_kw={"class": "btn btn-info btn-md"})

    def __init__(self, *args):
        super(AEZoneForm, self).__init__(*args)
        """下拉框默认值初始化"""
        self.game.choices = [(game.id, game.name) for game in
                             Games.query.all()]
        self.channel.choices = [(channel.id, channel.name) for channel in
                                Channels.query.all()]
