import datetime
import multiprocessing
import os
import time
import pdb
import subprocess
import zipfile
import pymysql
from slugify import slugify

from app.forms.game import AEChannelForm, AEGameForm, AEZoneForm
from app.models import Channels, Games, Membership, User, Zones, db
# from app.models import User
from flask import Blueprint, current_app, flash, jsonify, redirect, render_template, request, url_for
from flask_login import login_required
from app.util import myssh,bash
from app import basedir
try:
    import configparser
except:
    from six.moves import configparser

conf = configparser.RawConfigParser()

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
                     remote_initshell_path=form.remote_initshell_path.data,
                     local_open_service_pkg_path = form.local_open_service_pkg_path.data,
                     remote_open_service_pkg_path=form.remote_open_service_pkg_path.data,
                     remote_open_service_shell_path=form.remote_open_service_shell_path.data,
                     local_update_pkg_path = form.local_update_pkg_path.data,
                     remote_update_pkg_path = form.remote_update_pkg_path.data,
                     remote_hot_update_shell_path = form.remote_hot_update_shell_path.data,
                     remote_cold_update_shell_path = form.remote_cold_update_shell_path.data,

                     remote_startservice_shell_path = form.remote_startservice_shell_path.data,
                     remote_stopservice_shell_path = form.remote_stopservice_shell_path.data,

                     remote_unzip_path=form.remote_unzip_path.data)

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
                      remote_initshell_path=edit_game.remote_initshell_path,
                      local_open_service_pkg_path=edit_game.local_open_service_pkg_path,
                      remote_open_service_pkg_path=edit_game.remote_open_service_pkg_path,
                      remote_open_service_shell_path=edit_game.remote_open_service_shell_path,
                      local_update_pkg_path = edit_game.local_update_pkg_path,
                      remote_update_pkg_path = edit_game.remote_update_pkg_path,
                      remote_hot_update_shell_path = edit_game.remote_hot_update_shell_path,
                      remote_cold_update_shell_path = edit_game.remote_cold_update_shell_path,

                      remote_startservice_shell_path = edit_game.remote_startservice_shell_path,
                      remote_stopservice_shell_path = edit_game.remote_stopservice_shell_path,

                      remote_unzip_path=edit_game.remote_unzip_path
                      )

    if form.validate_on_submit():
        edit_game.name=form.name.data
        edit_game.local_initshell_path = form.local_initshell_path.data
        edit_game.remote_initshell_path = form.remote_initshell_path.data
        edit_game.local_open_service_pkg_path=form.local_open_service_pkg_path.data
        edit_game.remote_open_service_pkg_path=form.remote_open_service_pkg_path.data
        edit_game.remote_open_service_shell_path=form.remote_open_service_shell_path.data

        edit_game.local_update_pkg_path = form.local_update_pkg_path.data
        edit_game.remote_update_pkg_path = form.remote_update_pkg_path.data
        edit_game.remote_hot_update_shell_path = form.remote_hot_update_shell_path.data
        edit_game.remote_cold_update_shell_path = form.remote_cold_update_shell_path.data

        edit_game.remote_startservice_shell_path = form.remote_startservice_shell_path.data
        edit_game.remote_stopservice_shell_path = form.remote_stopservice_shell_path.data

        edit_game.remote_unzip_path=form.remote_unzip_path.data

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


@bp_game.route("/server_init",methods=["GET","POST"])
@login_required
def server_init():
    if request.method == "GET":
        games = Games.query.order_by("name")
        return render_template("game/server_init.html",games=games,title="服务初始化")

    else:
        gameid = request.json["gameid"]
        file_name = request.json["file_name"]
        iplists = request.json["iplists"].rstrip(',').split(',')
        gameobj = Games.query.get(gameid)

        """
        这里本来打算 用ansible来处理的，比较简单方便，但是输出不好看，太多冗余的信息，而且感觉ansible运行速度也达不到标准，
        使用ansible api 又会做太多处理，我是希望在点击执行之后能尽快执行脚本并且返回信息。
        """
        # cmd = "ansible -i '" + iplists + ",' all -m script -a " + os.path.join(gameobj.local_initshell_path, file_name)
        # print(cmd)
        # msg = ""
        # result = subprocess.Popen(cmd, stdin=subprocess.PIPE,
        #                           stdout=subprocess.PIPE,
        #                           stderr=subprocess.PIPE, shell=True)
        # for line in result.stdout.readlines():
        #     msg += line.decode("utf-8")
        # for line in result.stderr.readlines():
        #     msg += line.decode("utf-8")
        manager = multiprocessing.Manager()
        q = manager.dict()
        pool = multiprocessing.Pool(processes=len(iplists))
        for ip in iplists:
            # 目标服务器IP，脚本本地路径，脚本远端路径，脚本名，q
            pw = pool.apply_async(func_init, args=(ip, gameobj.local_initshell_path,gameobj.remote_initshell_path,file_name, q))
        pool.close()
        pool.join()

        total = output(q)

        return jsonify({"status":True,"msg":total})


def func_init(ip, local_initshell_path,remote_initshell_path,file_name, q):
    """
    服务初始化功能
    :param ip: 目标机器IP
    :param local_initshell_path: 本地脚本路径
    :param remote_initshell_path: 远端脚本路径
    :param file_name: 脚本名称
    :param q: Queue
    :return: Queue
    """
    ssh = myssh(ip)
    tmp = {}

    if ssh:
        """1、判断远端是否存在保存路径"""
        srp = "if [ ! -d '{dest_path}' ];then (mkdir -p {dest_path});fi;".format(dest_path=remote_initshell_path)
        ssh.exec_command(srp)

        """2、把脚本推送到远端"""
        pushcmd = "scp -pr -o StrictHostKeyChecking=no -i " + current_app.config["MYFLASKPROROOTKEY"] + " {src} root@{ip}:{dest};".format(ip=ip,
                    src=os.path.join(local_initshell_path, file_name),  dest=os.path.join(remote_initshell_path, file_name))
        bash(pushcmd)

        """3、执行shell，可能需要指定环境变量"""
        execute = "source /etc/profile;sh {shell}".format(shell=os.path.join(remote_initshell_path, file_name))
        stding,stdout,stderr = ssh.exec_command(execute)

        tmp["stdout"] = stdout.readlines()
        tmp["stderr"] = stderr.readlines()
        ssh.close()

    else:
        current_app.logger.error("shh连接错误")
        tmp["stderr"] = "shh连接错误"
        tmp["stdout"] = ""

    q[ip] = tmp


@bp_game.route("/get_gameinfo/",methods=["GET"])
@login_required
def get_gameinfo():
    gameid = request.args.get("gameid")
    type = request.args.get("type")

    game = Games.query.get(gameid)
    filename = slugify(game.name, to_lower=True, separator="") + ".md"
    files = []
    zips_ver = []
    channels_list = set()

    if type=="initshell":
        """获取初始化脚本"""
        try:
            dirs = os.listdir(game.local_initshell_path)
        except Exception as e:
            current_app.logger.error(e)
        else:
            files = [file for file in dirs if os.path.splitext(file)[-1] == ".sh"]

    elif type in ["openservice","updateprogram","updatedb","toggleservice"]:
        """开服选择游戏时返回对应渠道信息"""
        ms = Membership.query.filter_by(game_id=gameid)
        for i in ms:
            chanel = Channels.query.get(i.channel_id)
            channels_list.add((chanel.id,chanel.name))

        if type == "openservice":
            """获取本地开服版本包"""
            dirs = os.listdir(game.local_open_service_pkg_path)
        else:
            dirs = os.listdir(game.local_update_pkg_path)

        try:
            zips_ver = [zv for zv in dirs if zipfile.is_zipfile(os.path.join(game.local_open_service_pkg_path, zv))]
        except Exception as e:
            current_app.logger.error(e)

    """获取文档信息"""
    data = get_doc(filename,type)

    return jsonify({"files": files,
                    "zips_ver": zips_ver,
                    "channels_list": list(channels_list),
                    "pridoc": data})


@bp_game.route("/get_zoneinfo/",methods=["GET"])
@login_required
def get_zoneinfo():
    """
    参数游戏id，渠道id
    :return:
    """
    gameid= request.args.get("gameid")
    channelid= request.args.get("channelid")
    zones_list = []
    ip_list = ""
    ms = Membership.query.filter_by(game_id=gameid,channel_id=channelid)
    for i in ms:
        zone = Zones.query.get(i.zone_id)
        zones_list.append((zone.id,zone.zonename))

    return jsonify({"zones_list":zones_list})


def get_doc(filename,type):
    """获取该游戏文档信息"""
    docpath = os.path.join(basedir, "doc", type)
    if not os.path.exists(docpath):
        os.makedirs(docpath)

    docap = os.path.join(docpath, filename)
    if not (os.path.exists(docap) and os.path.isfile(docap)):
        with open(docap, "w") as w:
            w.write('NO DOC...')

    with open(docap, 'r') as r:
        data = r.read()

    return data


@bp_game.route("/get_script",methods=["POST"])
@login_required
def get_script():
    """
    游戏列表点击脚本编辑按钮弹出对应游戏对应功能的shell脚本
    :return:
    """
    game = request.json["game"]
    type = request.json["type"]

    filename = slugify(game, to_lower=True, separator="") + '.sh'

    """脚本文件夹路径"""
    thispath = os.path.join(basedir, "scripts", type)

    if not os.path.exists(thispath):
        os.makedirs(thispath)

    """脚本绝对路径"""
    scriptap = os.path.join(thispath, filename)

    if not (os.path.exists(scriptap) and os.path.isfile(scriptap)):
        with open(scriptap, "w") as w:
            w.write('#!/bin/bash')

    with open(scriptap, 'r') as r:
        data = r.read()
    return jsonify({"status": True, "msg": data})


@bp_game.route("/savecontent",methods=["POST"])
@login_required
def savecontent():
    content = request.json["content"]
    game = request.json["game"]
    type = request.json["type"]
    gameobj = Games.query.filter_by(name=game).first()

    filename = slugify(game, to_lower=True, separator="") + '.sh'

    """脚本文件夹路径"""
    thispath = os.path.join(basedir, "scripts", type)

    if not os.path.exists(thispath):
        os.makedirs(thispath)

    """脚本绝对路径"""
    scriptap = os.path.join(thispath, filename)

    try:
        if type == "hot_update":
            gameobj.local_hot_update_shell_path = scriptap
        elif type == "cold_update":
            gameobj.local_cold_update_shell_path = scriptap
        elif type == "startshell":
            gameobj.local_startservice_shell_path = scriptap
        elif type == "stopshell":
            gameobj.local_stopservice_shell_path = scriptap
        else:
            gameobj.local_open_service_shell_path = scriptap

        db.session.commit()
    except Exception as e:
        current_app.logger.error(e)

    with open(scriptap,'w') as f:
        f.write(content)

    return jsonify({"status":True})


@bp_game.route("/open_service",methods=["GET", "POST"])
@login_required
def open_service():
    """
    开服界面
    :return:
    """
    if request.method == "GET":
        games = Games.query.order_by("name")
        return render_template("game/open_service.html",games=games,title="新服搭建")

    else:
        game = Games.query.get(request.json["id_game"])
        channel = Channels.query.get(request.json["id_channel"])
        zonelist = request.json["id_zone"]
        version = request.json["id_version"]


        _dict =dict()
        for zone in zonelist:
            """处理一个ip有多个区服的情况"""
            zoneobj = Zones.query.get(zone)
            _dict.setdefault(zoneobj.zoneip,dict()).setdefault('zonename',list())
            _dict[zoneobj.zoneip]['zonename'].append(zoneobj.zonename)

        manager = multiprocessing.Manager()
        q = manager.dict()
        pool = multiprocessing.Pool(len(_dict))
        for k,v in _dict.items():
            """IP,zonename,game,q"""
            pw = pool.apply_async(func_openservi,args=(k,v,game,version,q))

        pool.close()
        pool.join()

        total = output(q)

        return jsonify({"status":True,"msg":total})


def func_openservi(zoneip,zonename,game,version,q):
    ssh = myssh(zoneip)
    tmp = {}

    if ssh:
        """1、判断远端是否存在保存发布包 和shell 路径"""
        srp = "if [ ! -d '{pkg_path}' ];then (mkdir -p {pkg_path});fi;if [ ! -d '{shell_path}' ];then (mkdir -p {shell_path});fi;".format(
            pkg_path=game.remote_open_service_pkg_path,shell_path=game.remote_open_service_shell_path)
        ssh.exec_command(srp)

        """2、把版本s推送到远端"""
        for ver in version:
            pushcmd = "scp -pr -o StrictHostKeyChecking=no -i " + current_app.config["MYFLASKPROROOTKEY"] + " {src} root@{ip}:{dest};".format(
            ip=zoneip,
            src=os.path.join(game.local_open_service_pkg_path, ver),
            dest=os.path.join(game.remote_open_service_pkg_path, ver))
            bash(pushcmd)

        """推送shell脚本"""
        # local_shell_path = os.path.join(basedir,"scripts","openshell")
        filename = slugify(game.name, to_lower=True, separator="") + '.sh'

        pushshell = "scp -pr -o StrictHostKeyChecking=no -i " + current_app.config["MYFLASKPROROOTKEY"] + " {src} root@{ip}:{dest};".format(
            ip=zoneip,
            src=game.local_open_service_shell_path,
            dest=os.path.join(game.remote_open_service_shell_path, filename))
        bash(pushshell)

        """3、解压发布包到指定目录"""
        cmd2 = ""
        cmd1 = "rm -rf {unzippath} && mkdir -p {unzippath} &&".format(unzippath=game.remote_unzip_path)
        for ver in version:
            cmd2 += "unzip -o -O CP936 -d {unzippath} {dest_version} >/dev/null 2>&1 &&".format(unzippath=game.remote_unzip_path,
                                                                                                dest_version=os.path.join(game.remote_open_service_pkg_path,ver))

        """4、执行脚本"""
        execute = "source /etc/profile;sh {shell}".format(
            shell=os.path.join(game.remote_open_service_shell_path, filename))

        stding, stdout, stderr = ssh.exec_command(cmd1 + cmd2 + execute)

        tmp["stdout"] = stdout.readlines()
        tmp["stderr"] = stderr.readlines()
        ssh.close()

    else:
        current_app.logger.error("shh连接错误")
        tmp["stderr"] = "shh连接错误"
        tmp["stdout"] = ""

    q[zoneip] = tmp
    
    
@bp_game.route("/update_program",methods=["GET","POST"])
@login_required
def update_program():
    """
    程序更新功能
    :return:
    """
    if request.method == "GET":
        games = Games.query.order_by("name")
        return render_template("game/update_program.html",games=games,title="程序更新")
    
    else:
        game = Games.query.get(request.json["id_game"])
        zoneids = request.json["id_zone"]
        version = request.json["id_version"]
        md5 = request.json["md5"]
        type = request.json["type"]

        _dict = dict()
        for id in zoneids:
            zone = Zones.query.get(id)
            _dict.setdefault(zone.zoneip,dict()).setdefault("zonename",list())
            _dict[zone.zoneip]["zonename"].append(zone.zonename)

        manager = multiprocessing.Manager()
        q = manager.dict()

        pool = multiprocessing.Pool(len(_dict))
        for k,v in _dict.items():
            """IP,区服名称，游戏对象，版本，md5,更新类型"""
            pw = pool.apply_async(func_updateprog,args=(k,v.get('zonename'),game,version,md5,type,q))

        pool.close()
        pool.join()

        total = output(q)

        return jsonify({"status": True, "msg": total})


def func_updateprog(ip, zonename, game, version, md5, style, q):
    """IP,区服名称，游戏对象，版本，md5,更新类型"""
    ssh = myssh(ip)
    tmp = {}
    if ssh:
        try:
            """1、判断远端是否存在保存发布包 和shell 路径"""
            srp = "if [ ! -d '{pkg_path}' ];then (mkdir -p {pkg_path});fi;if [ ! -d '{shell_path}' ];then (mkdir -p {shell_path});fi;".format(
                pkg_path=game.remote_update_pkg_path,
                shell_path=game.remote_hot_update_shell_path if style =="hot_udpate" else game.remote_cold_update_shell_path)
            ssh.exec_command(srp)

            """2、把版本和脚本推送到指定目录"""
            pushversion = "scp -pr -o StrictHostKeyChecking=no -i " + current_app.config["MYFLASKPROROOTKEY"] + " {src} root@{ip}:{dest};".format(
                ip=ip,
                src=os.path.join(game.local_update_pkg_path, version),
                dest=os.path.join(game.remote_update_pkg_path, version))

            filename = slugify(game.name, to_lower=True, separator="") + '.sh'

            pushshell = "scp -pr -o StrictHostKeyChecking=no -i " + current_app.config["MYFLASKPROROOTKEY"] + " {src} root@{ip}:{dest};".format(
                ip=ip,
                src=game.local_hot_update_shell_path if style =="hot_update" else game.local_cold_update_shell_path,
                dest=os.path.join(game.remote_hot_update_shell_path if style =="hot_update" else game.remote_cold_update_shell_path,filename))

            bash(pushversion + pushshell)

            """3、推送后校验MD5值"""
            i,o,e = ssh.exec_command('md5sum {remote_ver}'.format(remote_ver=os.path.join(game.remote_update_pkg_path,version)))
            if o.readlines()[0].split(' ')[0].upper() != md5.upper():
                raise Exception('版本md5值传输前后不一致，终止解压更新操作！\n')

            """4、解压发布包到指定目录"""
            cmd1 = "rm -rf {unzippath} && mkdir -p {unzippath} &&".format(unzippath=game.remote_unzip_path)
            cmd2 = "unzip -o -O CP936 -d {unzippath} {dest_version} >/dev/null 2>&1 &&".format(
                unzippath=game.remote_unzip_path,
                dest_version=os.path.join(game.remote_update_pkg_path, version))

            """5、执行脚本"""
            execute = "source /etc/profile;sh {shell}".format(
                shell=os.path.join(game.remote_hot_update_shell_path if type=="hot_update" else game.remote_cold_update_shell_path,filename))

            stding, stdout, stderr = ssh.exec_command(cmd1 + cmd2 + execute)

            tmp["stdout"] = stdout.readlines()
            tmp["stderr"] = stderr.readlines()
            ssh.close()
        except Exception as e:
            current_app.logger.error(e)
            tmp["stdout"] = ""
            tmp["stderr"] = str(e)

    else:
        current_app.logger.error("shh连接错误")
        tmp["stderr"] = "shh连接错误"
        tmp["stdout"] = ""

    q[ip] = tmp


def output(q):
    """
    格式化输出
    :param q:
    :return:
    """
    total = ""
    for key, value in q.items():
        total = total + '-------------' + key + '------------- \n'
        if value['stdout']:
            total = total + '【输出】： \n'
            for v in value['stdout']:
                total = total + v
            total += '\n'

        if value['stderr']:
            total = total + '【错误信息】： \n'
            for e in value['stderr']:
                total = total + e
            total += '\n'
        total += '\n\n'

    return total


@bp_game.route("/update_db",methods=["GET","POST"])
@login_required
def update_db():
    """
    数据库更新功能
    :return:
    """
    if request.method == "GET":
        games = Games.query.order_by("name")
        return render_template("game/update_db.html",title="数据库更新",games=games)
    else:
        try:
            zonelist = request.json["zoneid"]
            game = Games.query.get(request.json["gameid"])
            db = request.json["db"]
            
            conf.read(os.path.join(basedir,"instance/config.conf"))
            if not conf.has_section(game.name):
                raise Exception("没有该游戏数据库账号密码信息，请联系管理员")

            """格式化脚本"""
            sql = request.json["sql"].replace('\n',' ')
            res = sql.split(";")
            sql_list = list(filter(not_empty,res))

            manager = multiprocessing.Manager()
            q = manager.dict()
            pool = multiprocessing.Pool(processes=len(zonelist))

            for zone in zonelist:
                zoneobj = Zones.query.get(zone)
                if db == "DB_A":
                    dbbase = zoneobj.db_A
                elif db=="DB_B":
                    dbbase = zoneobj.db_B
                else:
                    dbbase = zoneobj.db_C

                pw = pool.apply_async(func_dbupdate,args=(zoneobj,game,dbbase,sql_list,q))

            pool.close()
            pool.join()

            total = ""
            """一台服务器可能有多个数据库，需要分类显示 """
            """ q 内容
            {"IP1-DB1":{"stdout":"content","stderr":"content"},"IP1-DB2":{"stdout":"content","stderr":"content"},"IP1-DB3":{"stdout":"content","stderr":"content"}.....}
            """
            """ 需要把q   内容转换为 
            {"IP1":{"DB1":{"stdout":"content","stderr":"content"},"DB2":{"stdout":"content","stderr":"content"},"DB3":{"stdout":"content","stderr":"content"}}.........}
            """
            q_format = {}
            for qk, qv in q.items():
                _ip, _db = qk.split("-")
                q_format.setdefault(_ip, dict()).setdefault(_db, dict())
                q_format[_ip][_db]["stdout"] = qv["stdout"]
                q_format[_ip][_db]["stderr"] = qv["stderr"]

            for key, value in q_format.items():
                total = total + '------------------ ' + key + ' ------------------ \n'
                for k, v in value.items():
                    total = total + '  >>>> ' + k + ' <<<< \n'
                    if v['stdout']:
                        total = total + '【输出】： \n'
                        for _v in v['stdout']:
                            total = total + _v
                        total += '\n'

                    if v['stderr']:
                        total = total + '【错误信息】： \n'
                        for e in v['stderr']:
                            total = total + e
                        total += '\n'
                total += '\n\n'

            status = True
            msg = "msg"
        except Exception as e:
            status = False
            total = str(e)
            current_app.logger.error(e)
        return jsonify({"status":status,"msg":total})


def func_dbupdate(zoneobj,game,dbbase,sql_list,q):
    tmp = {}
    account = conf.get(game.name, "ACCOUNT")
    psd = conf.get(game.name, "PASSWORD")
    try:
        conn = pymysql.connect(host=zoneobj.dblink,
                               port=int(zoneobj.dbport),
                               user=account,
                               password=psd,
                               database=dbbase,
                               charset="utf8")
    except Exception as e:
        tmp["stdout"] = ""
        tmp["stderr"] = str(e) + "\n"
        q[zoneobj.dblink + "-" + dbbase] = tmp

    try:
        cursor = conn.cursor()
        tmp["stdout"] = ""
        for sql in sql_list:
            n = cursor.execute(sql)
            tmp["stdout"] += '脚本：' + sql[:30] + " ... 执行完成, 影响 {num} 条数据;".format(num=n) + "\n"
        tmp["stderr"] = ""

        q[zoneobj.dblink + "-" + dbbase] = tmp

    except Exception as e:
        tmp["stdout"] = ""
        tmp["stderr"] = '脚本：' + sql[:30] + " ... 执行失败：{msg}，该库变更已回滚 ".format(msg=str(e)) + "\n"
        q[zoneobj.dblink + "-" + dbbase] = tmp
        conn.rollback()
    finally:
        conn.commit()
        conn.close()


def not_empty(s):
    """去除列表空值"""
    return s and s.strip()


@bp_game.route("/toggle_service",methods=["GET","POST"])
@login_required
def toggle_service():
    """
    启停游戏功能
    :return:
    """
    if request.method == 'GET':
        games = Games.query.order_by("name")
        return render_template("game/toggle_service.html",title="启停游戏",games=games)

    else:
        pass