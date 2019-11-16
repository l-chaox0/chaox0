#!/usr/bin/env python
# -*- coding:utf-8 -*-

import json, time, psutil
import os, zipfile, datetime
import ConfigParser
from ding_ding import DingDing
from conf_script import server_dir
from dbmysql import mysql_db, sql_server_db
from conf_script import db_host, db_port, db_user, db_pass, db_name, w_user, w_pass, w_host, sqs_port, backup_dir, ip, \
    project, yunwei_dir, yunwei_tmp


class myconf(ConfigParser.ConfigParser):
    """
    config配置文件大小写切换类
    """

    def __init__(self, defaults=None):
        ConfigParser.ConfigParser.__init__(self, defaults=None)

    def optionxform(self, optionstr):
        return optionstr


def ht_update_sql(cmd):
    """
    后台数据库update 函数
    :param cmd: sql语句
    :return:
    """
    try:
        db_init = mysql_db(db_host, int(db_port), db_user, db_pass, db_name)
        data = db_init.cur.execute(cmd)
        print('sql result %s' % data)
        db_init.close()
    except Exception as e:
        print(e)


def ht_select_sql(cmd):
    """
    后台数据库select 函数
    :param cmd: sql语句
    :return:
    """
    try:
        db_init = mysql_db(db_host, int(db_port), db_user, db_pass, db_name)
        db_init.cur.execute(cmd)
        select_data = db_init.cur.fetchall()
        return select_data
    except Exception as e:
        print(e)


def date_str_lawyer(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, '%Y%m%d')
        return True
    except ValueError:
        return False


def update_conf_ini(serverdir, serverid):
    """
    修改配置文件函数
    :param serverdir: 后端配置文件目录
    :param serverid: 区服serverid
    :return:
    """
    conf = myconf()
    conf.read(serverdir + "/Config.ini")
    conf.set("GameConf", "dwStopTimeOut", serverid)

    try:
        with open(serverdir + "/Config.ini", "w+") as f:
            conf.write(f)
    except ImportError:
        pass


def update_sdk_json(serverdir, domain, oper, oper_id):
    """
    生成后端sdk.json配置文件函数
    :param serverdir: 后端配置文件目录
    :param domain: 区服域名
    :param oper: 平台oper
    :param oper_id: 平台id
    :return:
    """
    data_json = [{
        "param": "",
        "url": "http://" + domain + ":8000/userVerify.php",
        "platefor_name": oper,
        "platefor_id": oper_id
    }]
    json_str = json.dumps(data_json, ensure_ascii=False, sort_keys=False, indent=4)
    with open(serverdir + "/sdklist.json", 'wb') as json_file:
        json_file.write(json_str)
    print(json_str)


def update_json_conf(serverdir, serveroper, serverid, port, wsa, wpass, gamedb, logdb, domain):
    """
    生成后端config.json配置文件函数
    :param serverdir: 后端配置文件目录
    :param operid: 平台id
    :param serverid: 区服id
    :param port: 基础端口
    :param wsa: sqlserver用户
    :param wpass: sqlserver密码
    :param gamedb: 区服game数据库
    :param logdb: 区服log数据库
    :param domain: 区服域名
    :return:
    """
    data_json = [{
        "bOffInvite": False,  # 表示是否关闭邀请码功能，一般设为false
        "bVerifySdk": True,  # 表示是否要用sdk验证，一般为true
        "sVerifyUrl": "http://" + domain + ":8000/userVerify.php",  # 回调地址
        "sServerName": serverid,  # 区服ID
        "nPlateformId": serveroper,  # 平台名称pid
        "nServerID": serverid,  # 区服ID
        "nKuafu": 0,  # 区服类型0游戏服，1跨服
        "sIP": "127.0.0.1",  # sql server地址
        "nPort": int(port) - 19,  # 基础端口
        "nGateCount": 1,  # 游戏运行网关个数
        "Dir": serverdir + '/'}, {  # 区服地址绝对路径
        "sDBIpAddr": "127.0.0.1",
        "nDBPort": 1433,  # sql server端口
        "sDBName": gamedb,  # sql server游戏库
        "sDBUser": wsa,  # sql server账号
        "sDBPsw": wpass}, {  # sql server密码
        "sPayDBIpAddr": "127.0.0.1",
        "nPayDBPort": 1433,
        "sPayDBName": gamedb,
        "sPayDBUser": wsa,
        "sPayDBPsw": wpass}, {
        "sLogDB_IP": "127.0.0.1",
        "nLogDB_PORT": 1433,
        "sLogDB_NAME": logdb,  # sql server日志库
        "sLogDB_USER": wsa,
        "sLogDB_PSW": wpass}]
    if int(serverid) > 40000 and int(serverid) < 60000:
        data_json[0]['nKuafu'] = 1
    json_str = json.dumps(data_json, ensure_ascii=False, sort_keys=False, indent=4)
    if os.path.exists(serverdir + '/Config.json'):
        os.remove(serverdir + '/Config.json')
    with open(serverdir + "/Config.json", 'a+') as json_file:
        json_file.write(json_str)
        # print(json_str)


def update_client_conf(clientdir, oper, serverid, operid, domain, host, user, passwd, dbname, log_db_name, server_port,
                       int_host='127.0.0.1', dbport='1433'):
    """
    生成前端json配置文件函数
    :param clientdir:前端文件路径
    :param oper: 平台
    :param serverid: 区服id
    :param operid: 平台id
    :param domain: 区服域名
    :param host: 当前外网ip
    :param user: 数据库登录账号
    :param passwd: 数据库访问密码
    :param dbname: game数据库
    :param log_db_name: log数据库
    :param server_port: 区服基础端口
    :param int_host: 内网地址
    :param dbport: 数据库访问端口
    :return:
    """
    data_json = {
        "serverid": serverid,
        "operid": operid,
        "oper": oper,
        "domain": domain,
        "host_ip": host,
        "dbuser": user,
        "dbpasswd": passwd,
        "dbport": dbport,
        "db_name": dbname,
        "log_db_name": log_db_name,
        "socket_host": int_host,
        "serverport": server_port,
        "config_dir": clientdir
    }

    if len(log_db_name.split('_')) == 6:
        main_cmd = "select merge_toid from admin_game_info where oper='%s' and serverid=%s" % (oper, serverid)
        main_data = ht_select_sql(main_cmd)
        merge_toid = main_data[0]['merge_toid']
        if merge_toid != 0:
            data_json['serverport'] = ''

    json_str = json.dumps(data_json, ensure_ascii=False, sort_keys=False, indent=4)
    if os.path.exists(clientdir + "/client_conf.json"):
        os.remove(clientdir + "/client_conf.json")

    with open(clientdir + "/client_conf.json", 'a+') as json_file:
        json_file.write(json_str)
        # print(json_str)


def conf_json_par(dir):
    """
    读取后端json配置文件函数
    :param dir: 后端配置文件绝对路径
    :return:
    """
    with open(dir + "/Config.json", "rb") as fk:
        data = fk.read()
        temp = json.loads(data)
        return temp


def server_switch(game_server, switch):
    """
    游戏服关闭、重启、重载函数
    :param game_server:区服后端目录
    :param switch: 控制开关stop start reload
    :return:
    """
    game_server_dir = server_dir + '/' + game_server
    # print(game_server_dir, switch)
    if os.path.exists(game_server_dir):
        res = os.system('C:/Python27/python.exe %s/scripts/%s.py' % (game_server_dir, switch))
        if res:
            print(game_server_dir + ' ' + switch + ' failed')
        else:
            print(game_server_dir + ' ' + switch + ' success')


def print_log_format(log):
    with open(yunwei_tmp + '/log/yunwei.log', 'a+') as f:
        f.write(log)


def sqlserver_update_sql(cmd, db):
    """
    本地数据库 update 函数
    :param cmd:sql语句
    :param db: 数据库名
    :return:
    """
    try:
        db_init = sql_server_db(w_host, int(sqs_port), w_user, w_pass, db)
        data = db_init.cur.execute(cmd)
        print('sqlserver result %s' % data)
        db_init.close()
    except Exception as e:
        print(e)


def sqlserver_select_sql(cmd, db):
    """
    本地数据库 select 函数
    :param cmd:sql语句
    :param db: 数据库名
    :return:
    """
    try:
        db_init = sql_server_db(w_host, int(sqs_port), w_user, w_pass, db)
        db_init.cur.execute(cmd)
        select_data = db_init.cur.fetchall()
        return select_data
    except Exception as e:
        print(e)


def check_python_package():
    try:
        import psutil
    except ImportError as e:
        print("要先安装包!!! python -m pip install psutil")
        import os
        p = os.popen("python -m pip install psutil")
        print(p.read())
        import psutil


def check_disk():
    cpu_liyonglv = psutil.cpu_percent()
    memory = psutil.virtual_memory()
    # print psutil.swap_memory()
    menory_used = memory.used / 1024 / 1024 / 1024
    menory_total = memory.total / 1024 / 1024 / 1024
    ab = float(menory_used) / float(menory_total) * 100
    print "内存使用情况:%.2f%%    CUP单点峰值%s%%" % (ab, cpu_liyonglv)

    disk = psutil.disk_partitions()
    for i in disk:
        if i.fstype != "":
            disk_use = psutil.disk_usage(i.device)
            disk_used = disk_use.used / 1024 / 1024 / 1024
            disk_free = disk_use.free / 1024 / 1024 / 1024
            disk_total = disk_use.total / 1024 / 1024 / 1024
            disk_percent = disk_use.percent
            if int(disk_percent) > 70:
                disk_err = "%s %s %s More than 70%% disk space!" % (ip, project, i.device)
                print
                disk_err
                dingfail = DingDing('', disk_err)
                dingfail.dingding()
            print "磁盘:%s    分区格式:%s     使用%sG    空闲%sG  共计%sG   使用率%s%%" % (
                i.device, i.fstype, disk_used, disk_free, disk_total, disk_percent)


def check_port(port):
    """
    端口检测函数
    :param port:需要检测的端口
    :return:
    """
    sum_res = int(os.popen("netstat -ano | grep -w %s | wc -l" % port).read().strip('\n').strip())
    if sum_res == 0:
        servers_err = "%s check port %s finished %s process" % (ip, port, sum_res)
        print(servers_err)
        dingfail = DingDing('', servers_err)
        dingfail.dingding()
        return True
    else:
        print('check port %s %s ok' % (port, sum_res))


def unzip_file(zip_src, dst_dir):
    read_file = zipfile.is_zipfile(zip_src)
    if read_file:
        fz = zipfile.ZipFile(zip_src, 'r')
        for file in fz.namelist():
            fz.extract(file, dst_dir)
    else:
        print('This is not zip')
        return 1


def check_servers(servers, sumid):
    """
    服务检查函数
    :param servers:服务名称
    :param sumid: 服务个数
    :return:
    """
    rungate = int(os.popen("ps -W | grep -w %s | grep RunGate | wc -l" % servers).read().strip('\n').strip())
    if rungate != 0:
        rungate = int(1)

    sum_res = int(os.popen("ps -W | grep -w %s | grep -v RunGate | wc -l" % servers).read().strip('\n').strip())
    if sum_res + rungate != sumid:
        if servers == "ServerManage.exe":
            ServerManage = "D:/game/ServerManage/"
            if not os.path.exists(ServerManage):
                os.makedirs(ServerManage)
                os.system('cp -R %s/* %s/.' % ('C:/ServerManage', ServerManage))
                os.system('chmod 777 -R %s' % ServerManage)
            os.popen('C:/PSTools/PsExec.exe -accepteula -s -i 1 -d D:/game/ServerManage/ServerManage.exe')

        elif servers == "notepad.exe":
            os.system('taskkill /F /IM notepad.exe')
        elif servers == "ServerManager.exe":
            os.system('taskkill /F /IM ServerManager.exe')
        elif servers == "nginx.exe" or servers == "php-cgi.exe":
            os.system("C:/wnmp/stop.bat")
            os.system("C:/wnmp/start.bat")
            servers_err = "%s check the %s start finished %s process, reboot has been performed" % (
                ip, servers, sum_res)

        servers_err = "%s check the %s start finished %s process" % (ip, servers, sum_res + rungate)
        print(servers_err)
        dingfail = DingDing('', servers_err)
        dingfail.dingding()
        return sum_res
    else:
        print('check %s %s ok' % (servers, sum_res))


def update_db_patch(dir, up_dblog_md5, up_dbgame_md5):
    """
    sql文件更新函数
    :param dir: 区服绝对路径
    :param up_dblog_md5: 更新log文件md5值
    :param up_dbgame_md5: 更新game文件md5值
    :return:
    """
    temp = conf_json_par(dir)
    json_gamedb = temp[1]['sDBName']
    json_logdb = temp[3]['sLogDB_NAME']
    log_patch = dir + '/Sql/log_patch.sql'
    game_patch = dir + '/Sql/game_patch.sql'

    if os.path.exists(dir + '/Sql/game_md5_file'):
        with open(dir + '/Sql/game_md5_file', 'r') as f1:
            game_md5_file = f1.read().rstrip('\n')
    else:
        game_md5_file = ""

    if os.path.exists(game_patch) and up_dbgame_md5 != game_md5_file:
        try:
            res = os.system('sqlcmd -U %s -P %s -d %s -i "%s"' % (w_user, w_pass, json_gamedb, game_patch))
            print(res)
            if res != 0:
                print('%s update_game_patch failed' % json_gamedb)
                exit()
            print('%s update_game_patch success' % json_gamedb)
            os.remove(game_patch)
            with open(dir + '/Sql/game_md5_file', 'w+') as f:
                f.write(up_dbgame_md5)
        except:
            print('%s update_game_patch failed' % json_gamedb)
    else:
        print('%s update_game_patch There is no consistency in this file or md5' % json_gamedb)

    if os.path.exists(dir + '/Sql/log_md5_file'):
        with open(dir + '/Sql/log_md5_file', 'r') as f2:
            log_md5_file = f2.read().rstrip('\n')
    else:
        log_md5_file = ""

    if os.path.exists(log_patch) and up_dblog_md5 != log_md5_file:
        try:
            res = os.system('sqlcmd -U %s -P %s -d %s -i "%s"' % (w_user, w_pass, json_logdb, log_patch))
            if res != 0:
                print('%s update_log_patch failed' % json_logdb)
                exit()
            print('%s update_log_patch success' % json_logdb)
            os.remove(log_patch)
            with open(dir + '/Sql/log_md5_file', 'w+') as f:
                f.write(up_dblog_md5)
        except:
            print('%s update_game_patch failed' % json_logdb)
    else:
        print('%s update_log_patch There is no consistency in this file or md5' % json_logdb)


def sqlserver_backup(db, server_backup_dir):
    """
    数据库备份函数
    :param db: 数据库名
    :param server_backup_dir: 备份路径
    :return:
    """

    if not os.path.exists(server_backup_dir):
        os.makedirs(server_backup_dir)
    if os.path.exists(server_backup_dir + '/' + db + '.bak'):
        os.remove(server_backup_dir + '/' + db + '.bak')
    res = os.system('sqlcmd -U %s -P %s -Q "backup database %s to DISK=\'%s/%s.bak\'"' % (
        w_user, w_pass, db, server_backup_dir, db))
    if res != 0:
        backup_err = "%s %s %s backup failed!" % (ip, project, db)
        print
        backup_err
        dingfail = DingDing('', backup_err)
        dingfail.dingding()
