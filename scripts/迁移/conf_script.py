#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import configparser
from urllib import request


pwd = os.getcwd()
configPath = os.path.join(pwd,"main.txt")
path = os.path.abspath(configPath)
#print(path,configPath)

conf = configparser.ConfigParser()
#filename = conf.read(pwd + '/main.txt')
conf.read(path)

def fun_project():
    project = conf.get("project", "project_name")
    return project


def fun_rsyncd():
    rsync_port = conf.get("rsync", "rsync_port")
    rsync_user = conf.get("rsync", "rsync_user")
    rsync_host = conf.get("rsync", "rsync_host")
    backup_host = conf.get("rsync", "backup_host")
    merger_host = conf.get("rsync", "merger_host")
    return rsync_port, rsync_user, rsync_host, backup_host, merger_host


def work_dir():
    yunwei = conf.get("work_dir", "yunwei_dir")
    yunwei_dir = yunwei + '/' + project
    yunwei_tmp = yunwei_dir + '/' + 'yunwei_tmp'
    game_dir = conf.get("work_dir", "game_dir")
    client_dir = conf.get("work_dir", "client_dir")
    backup_dir = conf.get("work_dir", "backup_dir")
    cyunwei_dir = conf.get("work_dir", "cyunwei_dir")

    sqlserver_dir = conf.get("work_dir", "sqlserver_dir")
    kaifu_list = "%s/kaifu_dir/kaifu.list" % (yunwei_dir)
    update_dir = cyunwei_dir + '/' + project + '/update_dir'
    server_list = "%s/update_dir/server.list" % (yunwei_dir)
    client_list = "%s/update_dir/client.list" % (yunwei_dir)
    game_db_file = "%s/kaifu_dir/%s_game.sql" % (yunwei_dir, project)
    game_log_file = "%s/kaifu_dir/%s_log.sql" % (yunwei_dir, project)

    return yunwei_dir, yunwei_tmp, game_dir, client_dir, update_dir, backup_dir, cyunwei_dir, kaifu_list, server_list, client_list, game_db_file, game_log_file, sqlserver_dir


def host_ip():
    get_ip_url = conf.get("project", "get_ip_url")
    ip = request.urlopen(get_ip_url).read().decode()
    return ip


def mysql_db():
    db_name = project + '_gm'
    w_user = conf.get("mysqldb", "w_user")
    w_pass = conf.get("mysqldb", "w_pass")
    w_host = conf.get("mysqldb", "w_host")
    db_port = conf.get("mysqldb", "db_port")
    db_user = conf.get("mysqldb", "db_user")
    db_pass = conf.get("mysqldb", "db_pass")
    db_host = conf.get("mysqldb", "db_host")
    sqs_port = conf.get("mysqldb", "sqs_port")

    return db_port, db_user, db_pass, db_host, db_name, w_user, w_pass, w_host, sqs_port


ip = host_ip()
project = fun_project()
rsync_port, rsync_user, rsync_host, backup_host, merger_host = fun_rsyncd()
db_port, db_user, db_pass, db_host, db_name, w_user, w_pass, w_host, sqs_port = mysql_db()
yunwei_dir, yunwei_tmp, game_dir, client_dir, update_dir, backup_dir, cyunwei_dir, kaifu_list, server_list, client_list, game_db_file, game_log_file, sqlserver_dir = work_dir()
#print(db_host,sqs_port)
#print(yunwei_dir)