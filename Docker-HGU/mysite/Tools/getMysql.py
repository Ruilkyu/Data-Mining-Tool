# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
import pymysql.cursors
import json
import logging.handlers
import logging
import datetime, time
import os, sys
from django.db import connections

############数据库查询模块#########
class mysqlProcess:
    #获取本地数据库数据
    def getSQLData(str_sql):
        cur=connections['default'].cursor()
        cur.execute(str_sql)
        index = cur.description
        result = []
        for res in cur.fetchall():
            row = {}
            for i in range(len(index)):
                if type(res[i])==int:
                   row[index[i][0]] = res[i]
                elif type(res[i])==float:
                   row[index[i][0]] = res[i]
                else:
                   row[index[i][0]] = str(res[i]).replace('\r','')
            result.append(row)
        return result;

    #获取221.181.32.127拨测数据库数据
    def getSQLBoCeData(str_sql):
        cur=connections['boCeDB'].cursor()
        cur.execute(str_sql)
        index = cur.description
        result = []
        for res in cur.fetchall():
            row = {}
            for i in range(len(index)):
                if type(res[i])==int:
                   row[index[i][0]] = res[i]
                elif type(res[i])==float:
                   row[index[i][0]] = res[i]
                else:
                   row[index[i][0]] = str(res[i]).replace('\r','')
            result.append(row)
        return result;

    #更新数据库数据
    def updateSQLData(str_sql):
        cur = connections['default'].cursor()
        cur.execute(str_sql)
        connections['default'].commit()
        print ("update OK")
        return 1 

    def QueryMultiRecord(str_sql,strDBAlias):
        cur=connections[strDBAlias].cursor()
        cur.execute(str_sql)
        index = cur.description
        result = []
        for res in cur.fetchall():
            row = {}
            for i in range(len(index)):
                if type(res[i])==int:
                   row[index[i][0]] = res[i]
                elif type(res[i])==float:
                   row[index[i][0]] = res[i]
                else:
                   row[index[i][0]] = str(res[i])
            result.append(row)
        return result;
