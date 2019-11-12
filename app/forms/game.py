from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,HiddenField,TextAreaField,SelectField
from wtforms.validators import DataRequired,Optional
from app.models import Games,Channels


class AEGameForm(FlaskForm):
    id = HiddenField("id", validators=[Optional()])
    name = StringField("游戏", validators=[DataRequired()])
    local_initshell_path = StringField("本地初始化脚本路径",
                                       validators=[DataRequired()])
    remote_initshell_path = StringField("远端初始化脚本路径",
                                        validators=[DataRequired()])

    submit = SubmitField("Submit")


class AEChannelForm(FlaskForm):
    """
    新增/编辑 channel 表单
    """
    id = HiddenField("id", validators=[Optional()])
    name = StringField("渠道", validators=[DataRequired()])

    remark = TextAreaField("备注")

    submit = SubmitField("Submit")


class AEZoneForm(FlaskForm):
    """
    新增/编辑 zone 表单
    """
    id = HiddenField("id", validators=[Optional()])
    game = SelectField("游戏", coerce=int)
    channel = SelectField("渠道", coerce=int)

    zonenum = StringField("区服号", validators=[DataRequired()])
    zonename = StringField("区服名", validators=[DataRequired()])
    zoneip = StringField("区服IP", validators=[DataRequired()])
    dblink = StringField("数据库链接", validators=[DataRequired()])
    dbport = StringField("数据库端口", validators=[DataRequired()])
    db_A = StringField("数据库A", validators=[DataRequired()])
    db_B = StringField("数据库B", validators=[Optional()])
    db_C = StringField("数据库C", validators=[Optional()])

    submit = SubmitField("Submit")

    def __init__(self, *args):
        super(AEZoneForm, self).__init__(*args)
        """下拉框默认值初始化"""
        self.game.choices = [(game.id, game.name) for game in
                             Games.query.all()]
        self.channel.choices = [(channel.id, channel.name) for channel in
                                Channels.query.all()]
