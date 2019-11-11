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


association_game_channel = db.Table('association_game_channel',
                                    db.Column('game_id',db.Integer,db.ForeignKey('t_games.id')),
                                    db.Column('channel_id',db.Integer,db.ForeignKey('t_channels.id')))


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

    channels = db.relationship('Channels',secondary=association_game_channel, backref=db.backref("games"),lazy="dynamic")

    def __repr__(self):
        return '<Game {}>'.format(self.name)


class Channels(db.Model):
    """
    渠道表
    与区服表为 一对多关系
    """
    __tablename__ = "t_channels"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(length=30),unique=True)
    remark = db.Column(db.Text(length=500))
    zones = db.relationship("Zones", backref='channel', lazy="dynamic")

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

    channel_id = db.Column(db.Integer, db.ForeignKey('t_channels.id'))

    def __repr__(self):
        return '<Zone {}>'.format(self.zonename)
