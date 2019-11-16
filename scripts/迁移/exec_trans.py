#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys,os,configparser,time,json,gzip
from dbmysql import mysql_db,sql_server_db
from conf_script import rsync_port, rsync_user, rsync_host, project, ip, yunwei_dir, kaifu_list, db_host, db_port, \
    db_user, db_pass, db_name, w_user, w_pass, w_host, sqs_port, game_dir, client_dir, cyunwei_dir, yunwei_tmp, \
    server_list, client_list, sqlserver_dir, update_dir, merger_host

#import dbmysql

def trans_src_tar(src_ip,params=None):
    """
    执行源迁移服务器停服及备份&&传输到中心服
    :return:
    """
    mysql_init = mysql_db(db_host,int(db_port),db_user,db_pass,db_name)
    SERVER_DIRS = "select server_dir from admin_game_info where client_serverip='%s' and merge_toid=0" % src_ip
    server_dirs = mysql_init.fetch_all(SERVER_DIRS)
    print(server_dirs)
    localtime = (time.strftime('%Y%m%d', time.localtime(time.time())))
    server_backup_dir = '/'.join([yunwei_tmp,localtime])
    for game_server in server_dirs:
    ##    server_switch(game_server["server_dir"],"stop")
        config_file = "/".join([game_dir,game_server["server_dir"],"Config.json"])
        print(config_file)
        with open(config_file, 'r') as f:
            data = json.load(f)
        game_db = data[1]["sDBName"]
        sqlserver_backup.backup_one(game_db)
        game_server_gz = '.'.join([server_backup_dir,game_server["server_dir"],'gz'])
        g = gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=open(game_server_gz, 'wb'))
        g.write(open('E:\\python\\shzb\\迁移\\main.cfg', "rb").read())
        g.close()


    DB_PREFIX = "".join(["'",project,"_%","'"])
    #sqlserver_init = sql_server_db(w_host, int(sqs_port), w_user, w_pass)
    sqlserver_init = sql_server_db(src_ip, int(sqs_port), w_user, w_pass)

    show_gamedb = "select name,'%s',name from dbo.sysdatabases where name like %s" % (server_backup_dir,DB_PREFIX)
    #show_gamedb = "select name from dbo.sysdatabases where name=%s" % "zb37_ad_jz2_game_90003"
    game_db = sqlserver_init.fetch_all(show_gamedb)

    print(server_backup_dir,SERVER_DIRS,server_dirs,DB_PREFIX,show_gamedb, game_db,sep="\n")



    #GAME_DBS = os.system(GAME_DB_SQL)






def server_switch(game_server,switch):
    """
    游戏服启动/关闭函数
    :param game_server: 游戏服server_list
    :param switch: stop|start
    :return: 
    """
    str = "/"
    #print(game_server)
    game_server_dir = str.join([game_dir,game_server])

    print(game_server_dir)
    if os.path.exists(game_server_dir):

        #res = os.system('C:/Python3/python.exe %s/scripts/%s.py' % (game_server_dir,switch))
        res = "qq"
        print(res)
        if res:
            print(' '.join([game_server, switch, "failed"]))
        else:
            print(' '.join([game_server, switch, " success"]))

def sqlserver_backup(db,server_backup_dir):
    """
    sqlserver数据库备份函数
    :param db: 数据库名
    :param server_backup_dir: 备份路径
    :return:
    """
    db_bak = "/".join([server_backup_dir,db,".bak"])
    if not os.path.exists(server_backup_dir):
        os.makedirs(server_backup_dir)
    if os.path.exists(db_bak):
        os.remove(db_bak)
    #res = os.system('sqlcmd -U %s -P %s -Q "backup database %s to DISK=\'%s/%s.bak\'"' % (w_user,w_pass,db,server_backup_dir,db))
    sqlserver_init = sql_server_db(w_host, int(sqs_port), w_user, w_pass)
    backup_sql = "backup database %s to DISK=\'%s/%s.bak\'" % (db,server_backup_dir,db)
    res = sqlserver_init.execute_many(backup_sql)

    if res != 0:
        backup_err = "%s %s %s backup failed" % (ip,project,db)
        print(backup_err)

class sqlserver_backup:
    """
    sqlserver数据库备份
    """

    def __init__(self,backup_dir):
        self.sqlserver_init = sql_server_db(w_host, int(sqs_port), w_user, w_pass)
        self.server_backup_dir = backup_dir
        if not os.path.exists(self.server_backup_dir):
            os.makedirs(self.server_backup_dir)


    def backup_one(self,db):
        # res = os.system('sqlcmd -U %s -P %s -Q "backup database %s to DISK=\'%s/%s.bak\'"' % (w_user,w_pass,db,server_backup_dir,db))
        self.db_bak = "".join(["/".join([self.server_backup_dir, db]), ".bak"])
        if os.path.exists(self.db_bak):
            os.remove(self.db_bak)

        self.backup_sql = "backup database %s to DISK=\'%s/%s.bak\'" % (db, self.server_backup_dir, db)
        self.res = self.sqlserver_init.execute_one(self.backup_sql)
        if self.res != 0:
            self.backup_err = "%s %s %s backup failed" % (ip, project, db)
            print(self.backup_err)

    def backup_many(self,db_list):
        #backup_sql = "backup database %s to DISK=\'%s/%s.bak\'" % (db, server_backup_dir, db)
        #self.db = [('zb37_ad_jz2_game_103_n2',), ('zb37_ad_jz2_game_90001',), ('zb37_ad_jz2_game_90002',)]
        self.db_list = db_list
        for db in self.db_list:
            self.db_bak = "".join(["/".join([self.server_backup_dir, db[0]]), ".bak"])
            if os.path.exists(self.db_bak):
                os.remove(self.db_bak)

        self.backup_sql = "backup database %s to DISK=\'%s/%s.bak\'"
        self.res = self.sqlserver_init.execute_many(self.backup_sql,db_list)


#c = sqlserver_backup

trans_src_tar("47.111.160.167")
