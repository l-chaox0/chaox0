#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os,re,sys
while True:
    try:
        import requests,bs4,xlwt,xlrd,xlutils
        break
    except:
        os.system('pip install requests bs4 xlwt xlrd xlutils')
        continue
from bs4 import BeautifulSoup
from xlrd import open_workbook
from xlutils.copy import copy

def get_data(url):
    req = requests.get(url)
    soup = BeautifulSoup(req.text,'lxml')
    ans = soup.find_all('title')
    ans1 = soup.find(name='span',attrs={'class':"c-text"},text=re.compile("\d+"))
    ans2 = soup.find_all(text=re.compile("人民法院"))
    title = str(ans[0].string).split(' ', 1)
    phone = str(ans1.string).strip()
    comp = ans2[0].string.strip()
    return title[0],comp,phone

def write_file(data):
    r_xls = open_workbook("est.xls")
    row = r_xls.sheets()[0].nrows
    excel = copy(r_xls)
    table = excel.get_sheet(0)
    #print(len(data))
    for i in range(len(data)):
        table.write(row, i, data[i])
    excel.save("est.xls")

with open('url.txt','r') as fn:

    for line in fn.readlines():
        a = get_data(line)
        # print(a)
        write_file(a)