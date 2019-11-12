from app.apis.api import PyCrypt
from app.forms.game import AEGameForm,AEChannelForm,AEZoneForm
from app.models import User, db, Games,Channels,Zones,Membership
# from app.models import User
from flask import Blueprint, current_app, flash, jsonify, redirect, \
    render_template, request, url_for
from flask_login import login_required

bp_game = Blueprint("bp_game", __name__, url_prefix="/game")


@bp_game.route("/games_list",methods=["GET"])
@login_required
def games_list():
    # games = Games.query.order_by("name")
    return render_template("game/games_list.html")


@bp_game.route("/get_games",methods=["GET"])
@login_required
def get_games():
    _table = []
    games = Games.query.order_by("name")
    for idx, game in enumerate(games,1):
        tmp={}
        tmp["idx"] = idx
        tmp["name"] = game.name
        _table.append(tmp)
        
    return jsonify(_table)


@bp_game.route("/create_game",methods=["GET","POST"])
@login_required
def create_game():
    form = AEGameForm()
    if form.validate_on_submit():
        game = Games(name=form.name.data,
                     local_initshell_path=form.local_initshell_path.data,
                     remote_initshell_path=form.remote_initshell_path.data)

        db.session.add(game)
        try:
            db.session.commit()
            flash("添加成功", "alert-info")
            return redirect(url_for('.games_list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(e, "alert-danger")
    return render_template("createdit_module.html", form=form,title="新增游戏")


@bp_game.route("/del_game",methods=["POST"])
@login_required
def del_game():
    name = request.form.get("name", "")
    game = Games.query.filter_by(name=name).first()
    if game:
        db.session.delete(game)
        db.session.commit()
        e = True
    return jsonify({"e": e, "msg": "succeed"})


@bp_game.route("/edit_game/<name>", methods=["GET", "POST"])
@login_required
def edit_game(name):
    edit_game = Games.query.filter_by(name=name).first()
    form = AEGameForm(id=edit_game.id,
                      name=edit_game.name,
                      local_initshell_path=edit_game.local_initshell_path,
                      remote_initshell_path=edit_game.remote_initshell_path)

    if form.validate_on_submit():
        edit_game.name=form.name.data
        edit_game.local_initshell_path = form.local_initshell_path.data
        edit_game.remote_initshell_path = form.remote_initshell_path.data

        try:
            db.session.commit()
            flash("修改成功", "alert-info")
            return redirect(url_for('.games_list'))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(e, "alert-danger")

    return render_template("createdit_module.html",form=form,title="编辑游戏")


@bp_game.route("/channels_list",methods=["GET"])
@login_required
def channels_list():
    return render_template("game/channels_list.html")


@bp_game.route("/get_channels",methods=["GET"])
@login_required
def get_channels():
    _table = []
    channels = Channels.query.order_by("name")

    for idx,channel in enumerate(channels,1):
        tmp = {}
        tmp["idx"] = idx
        tmp["name"] = channel.name
        _table.append(tmp)

    return jsonify(_table)


@bp_game.route("/create_channel", methods=["GET", "POST"])
@login_required
def create_channel():
    form = AEChannelForm()
    if form.validate_on_submit():
        channel = Channels(name=form.name.data,remark=form.remark.data)
        db.session.add(channel)
        try:
            db.session.commit()
            flash("添加成功","alert-info")
            return redirect(url_for(".channels_list"))
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(e)
            flash(e, "alert-danger")
            
    return render_template("createdit_module.html", form=form,title="新增渠道")


@bp_game.route("/del_channel", methods=["GET", "POST"])
@login_required
def del_channel():
    name = request.form.get("name", "")
    channel = Channels.query.filter_by(name=name).first()
    if channel:
        db.session.delete(channel)
        db.session.commit()
        e = True
    return jsonify({"e": e, "msg": "succeed"})


@bp_game.route("/edit_channel/<name>",methods=["GET","POST"])
@login_required
def edit_channel(name):
    channel = Channels.query.filter_by(name=name).first()
    form = AEChannelForm(id=channel.id, name=channel.name,
                         remark=channel.remark)

    if form.validate_on_submit():
        channel.name = form.name.data
        channel.remerk = form.remark.data
        try:
            db.session.commit()
            flash("编辑成功","alert-info")
            return redirect(url_for(".channels_list"))
        except Exception as e:
            db.session.rollback()
            flash(e,"alert-danger")

    return render_template("createdit_module.html", form=form, title="编辑渠道")


@bp_game.route("/zones_list",methods=["GET"])
@login_required
def zones_list():
    return render_template("game/zones_list.html")


@bp_game.route("/get_zonelist",methods=["GET"])
def get_zonelist():
    _table = []
    memberships = Membership.query.all()
    for idx,ms in enumerate(memberships,1):
        tmp = {}
        tmp["idx"] = idx
        tmp["zone_id"] = ms.zone_id
        tmp["game"] = Games.query.get(ms.game_id).name
        tmp["channel"] = Channels.query.get(ms.channel_id).name
        tmp["zonename"] = Zones.query.get(ms.zone_id).zonename
        _table.append(tmp)

    return jsonify(_table)


@bp_game.route("/create_zone/", methods=["GET", "POST"], defaults={"zone_id": ""})
@bp_game.route("/create_zone/<zone_id>", methods=["GET", "POST"])
@login_required
def create_zone(zone_id):
    if zone_id:
        """拷贝"""
        title = "拷贝区服"
        membership = Membership.query.filter_by(zone_id=zone_id).first()
        zone = Zones.query.get(zone_id)
        form = AEZoneForm(game=membership.game_id,
                          channel=membership.channel_id,
                          zonenum=zone.zonenum, zonename=zone.zonename,
                          zoneip=zone.zoneip,
                          dblink=zone.dblink, dbport=zone.dbport,
                          db_A=zone.db_A,
                          db_B=zone.db_B, db_C=zone.db_C)

    else:
        """新增"""
        title = "新增区服"
        form = AEZoneForm()

    if form.validate_on_submit():
        game = Games.query.get(form.game.data)
        channel = Channels.query.get(form.channel.data)
        zones = Zones(zonenum=form.zonenum.data,
                      zonename=form.zonename.data,
                      zoneip=form.zoneip.data,
                      dblink=form.dblink.data,
                      dbport=form.dbport.data,
                      db_A=form.db_A.data,
                      db_B=form.db_B.data,
                      db_C=form.db_C.data)

        try:
            # 先保存区服对象
            db.session.add(zones)
            db.session.commit()

            membership = Membership(game, channel, zones)
            db.session.add(membership)
            db.session.commit()
            flash("操作成功", "alert-info")
            return redirect(url_for(".zones_list"))
        except Exception as e:
            db.session.rollback()
            flash(e, "alert-danger")
    return render_template("createdit_module.html", form=form, title=title)


@bp_game.route("/del_zone", methods=["POST"])
@login_required
def del_zone():
    zone_id = request.form.get("zone_id", "")
    membership = Membership.query.filter_by(zone_id=zone_id).first()
    zone = Zones.query.get(zone_id)
    # 以下删除顺序 需要先删除关系表，在删除zone 表数据
    db.session.delete(zone)
    db.session.delete(membership)

    db.session.commit()
    return jsonify({"e": True, "msg": "succeed"})


@bp_game.route("/edit_zone/<int:zone_id>", methods=["GET", "POST"])
@login_required
def edit_zone(zone_id):
    zid = zone_id
    membership = Membership.query.filter_by(zone_id=zid).first()
    zone = Zones.query.get(zid)
    form = AEZoneForm(id=zid, game=membership.game_id,
                      channel=membership.channel_id,
                      zonenum=zone.zonenum, zonename=zone.zonename,
                      zoneip=zone.zoneip,
                      dblink=zone.dblink, dbport=zone.dbport, db_A=zone.db_A,
                      db_B=zone.db_B, db_C=zone.db_C)

    if form.validate_on_submit():
        membership.game_id = form.game.data
        membership.channel_id = form.channel.data
        zone.zonenum = form.zonenum.data
        zone.zonename = form.zonename.data
        zone.zoneip = form.zoneip.data
        zone.dblink = form.dblink.data
        zone.dbport = form.dbport.data
        zone.db_A = form.db_A.data
        zone.db_B = form.db_B.data
        zone.db_C = form.db_C.data
        try:
            db.session.commit()
            flash("操作成功","alert-info")
            return redirect(url_for('bp_game.zones_list'))
        except Exception as e:
            db.session.rollback()
            flash(e,"alert-danger")

    return render_template("createdit_module.html", form=form,title="编辑区服")

