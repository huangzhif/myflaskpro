from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db,login_manager
from hashlib import md5


class User(UserMixin, db.Model):
    __tablename__ = "t_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_active = db.Column(db.Boolean)

    def avatar(self, size=36):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)


@login_manager.user_loader
def load_user(id):
    """
    注册回调函数
    :param id:
    :return:
    """
    return User.query.get(int(id))


# 关联表与区服表是
# association_game_channel = db.Table('association_game_channel',
#                                     db.Column('game_id',db.Integer,db.ForeignKey('t_games.id')),
#                                     db.Column('channel_id',db.Integer,db.ForeignKey('t_channels.id')))

class Membership(db.Model):
    """
    整个表可以认为zone_id 就是主键，因为逻辑是先保存zone表数据，才有zone_id,
    所有数据zone_id绝对不会有重复值，
    所以在删除的时候，需要以zone_id 查询，先删除该表数据，再删除zone表数据。
    """
    game_id = db.Column(db.Integer, db.ForeignKey('t_games.id'), primary_key=True)
    channel_id = db.Column(db.Integer, db.ForeignKey('t_channels.id'), primary_key=True)
    zone_id = db.Column(db.Integer, db.ForeignKey("t_zones.id"), primary_key=True)

    db.UniqueConstraint('game_id','channel_id','zone_id')
    db.relationship('Games',uselist=False,backref='memberships',lazy='dynamic')
    db.relationship('Channels',uselist=False,backref='memberships',lazy='dynamic')
    db.relationship('Zones',uselist=False,backref='memberships',lazy='dynamic')

    def __init__(self,game,channel,zone):
        self.game_id = game.id
        self.channel_id = channel.id
        self.zone_id = zone.id

    def __repr__(self):
        return "<Membership %s, %s, %s>" % (self.game_id,self.channel_id,self.zone_id)


class Games(db.Model):
    """
    游戏表
    与渠道表 为 多对多关系
    """
    __tablename__ = "t_games"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=50), unique=True)

    local_initshell_path = db.Column(db.String(length=200))
    remote_initshell_path = db.Column(db.String(length=200))

    local_open_service_pkg_path = db.Column(db.String(length=200))
    local_open_service_shell_path = db.Column(db.String(length=200))

    remote_open_service_pkg_path = db.Column(db.String(length=200))
    remote_open_service_shell_path = db.Column(db.String(length=200))

    local_update_pkg_path = db.Column(db.String(length=200))
    local_hot_update_shell_path = db.Column(db.String(length=200))
    local_cold_update_shell_path = db.Column(db.String(length=200))

    remote_update_pkg_path = db.Column(db.String(length=200))
    remote_hot_update_shell_path = db.Column(db.String(length=200))
    remote_cold_update_shell_path = db.Column(db.String(length=200))

    local_startservice_shell_path = db.Column(db.String(length=200))
    local_stopservice_shell_path = db.Column(db.String(length=200))
    remote_startservice_shell_path = db.Column(db.String(length=200))
    remote_stopservice_shell_path = db.Column(db.String(length=200))

    remote_unzip_path = db.Column(db.String(length=200))

    # channels = db.relationship('Channels',secondary=association_game_channel, backref=db.backref("games"),lazy="dynamic")

    def __repr__(self):
        return '<Game {}>'.format(self.name)


class Channels(db.Model):
    """
    渠道表
    """
    __tablename__ = "t_channels"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(length=30),unique=True)
    remark = db.Column(db.Text(length=500))
    # zones = db.relationship("Zones", backref='channel', lazy="dynamic")

    def __repr__(self):
        return '<Channel {}>'.format(self.name)


class Zones(db.Model):
    """
    区服表
    """
    __tablename__ = "t_zones"
    id = db.Column(db.Integer, primary_key=True)
    zonenum = db.Column(db.String(length=30))
    zonename = db.Column(db.String(length=30))
    zoneip = db.Column(db.String(length=30))
    dblink = db.Column(db.String(length=30))
    dbport = db.Column(db.Integer)
    db_A = db.Column(db.String(length=10))
    db_B = db.Column(db.String(length=10))
    db_C = db.Column(db.String(length=10))

    # channel_id = db.Column(db.Integer, db.ForeignKey('t_channels.id'))

    def __repr__(self):
        return '<Zone {}>'.format(self.zonename)
