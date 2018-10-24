from django.shortcuts import render
from django.http import HttpResponse

import time
import json
import csv
from Tools.getMysql import mysqlProcess as DB


# Create your views here.
# 定义一些方法
# 统计表中记录数
def getTotalCount(tableName):
    sql = "select count(*) as cnt from %s" % (tableName)
    result = DB.getSQLData(sql)
    #print(result[0]['cnt'])
    if result == []:
        return 0
    return result[0]['cnt']


# 脱敏处理
def desensitization(data):
    i = 3
    ret = ''
    if data != 'unknown':
        if i < len(data):
            ret = data[0:3]
            ret += "********"
        return ret
    return data


# 1、获取网关信息列表，对应数据库表：HGUPeriodic_sum（时粒度表），HGUPeriodic_sum_sumDay（天粒度表）
def getGatewayListInfo(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []
    result1 = []
    condition = ''

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        endtime = request.GET.get('endTime')
        timeInterval = request.GET.get('timeInterval')
        deviceId = request.GET.get('deviceid')
        cityid = request.GET.get('cityId')
        start = request.GET.get('start')
        limit = request.GET.get('limit')
        page = request.GET.get('page')
        if timeInterval == '3600':
            tableName = "HGUPeriodic_sum"
        elif timeInterval == '86400':
            tableName = "HGUPeriodic_sum_sumDay"

        if deviceId != '':
            condition = "AND deviceid = '%s'"%(deviceId)
            if cityid == '0':
                sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s %s LIMIT %s,%s;" % (tableName, begintime, endtime, condition, start, limit);
                print(sql)
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s %s;" % (tableName, begintime, endtime, condition);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
            else:
                sql = "SELECT * FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s LIMIT %s,%s;" % (tableName, cityid, begintime, endtime,condition ,start, limit);
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s;" % (tableName, cityid, begintime, endtime, condition);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
        else:
            if cityid == '0':
                sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s LIMIT %s,%s;" % (tableName, begintime, endtime, start, limit);
                print(sql)
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s;" % (tableName, begintime, endtime);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
            else:
                sql = "SELECT * FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s LIMIT %s,%s;" % (tableName, cityid, begintime, endtime, start, limit);
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s;" % (tableName, cityid, begintime, endtime);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
    totalCount = result1[0]['cnt']
    for index in range(len(rows)):
        tmp = rows[index]['PPPOEUser']
        if len(tmp) == 11:
            tmp = tmp[0:3] + '********'
        rows[index]['PPPOEUser'] = tmp
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")


# 2、获取详细信息
def getGatewayDetailInfo(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []
    result1 = []
    condition = ''


    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        endtime = request.GET.get('endTime')
        timeInterval = request.GET.get('timeInterval')
        Type = request.GET.get('type')
        deviceId = request.GET.get('deviceid')
        start = request.GET.get('start')
        limit = request.GET.get('limit')


        if Type == 'wannumber':
            if int(timeInterval) == 3600:
                tableName = "HGUPeriodic_wan_sum"
            elif int(timeInterval) == 86400:
                tableName = "HGUPeriodic_wan_sum_sumDay"
        elif Type == 'subdevicenumber':
            if int(timeInterval) == 3600:
                tableName = "HGUPeriodic_subdevice_sum"
            elif int(timeInterval) == 86400:
                tableName = "HGUPeriodic_subdevice_sum_sumDay"

        if deviceId != '':
            condition = "AND deviceid = '%s'" %(deviceId)
            sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s %s LIMIT %s,%s;" % (
                tableName, int(begintime), int(endtime), condition, start, limit)
            print(sql)
            sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s %s;" % (
                tableName, int(begintime), int(endtime), condition)
            print(sql1)
            result = DB.getSQLData(sql)
            result1 = DB.getSQLData(sql1)
            rows = result
            if result == []:
                nErrorCode = 1
            print("how are you!")
        else:
            sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s  LIMIT %s,%s;" % (
                tableName, int(begintime), int(endtime), start, limit)
            sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s;" % (
                tableName, int(begintime), int(endtime))
            result = DB.getSQLData(sql)
            result1 = DB.getSQLData(sql1)
            rows = result
            if result == []:
                nErrorCode = 1
            print("I am fine!")
        print("hi,nice to meet you!")
    totalCount = result1[0]['cnt']
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")



# 3、获取汇总数据，对应数据库表：HGUPeriodic_city_sum_sumDay(天粒度表)
def getHGUIndexInfo(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        tableName = "HGUPeriodic_city_sum_sumDay"
        column = "reportTime,citycode,cityId,sum(hguCnt) as hguCnt ,sum(cpurate) as  cpurate ,sum(ramrate) as " \
                    "ramrate,sum(ponrxpower) as ponrxpower,"\
                    + "sum(weaklightUsers) as weaklightUsers, sum(pppoesuccessnumber) as pppoesuccessnumber ,"\
                    + "sum(wirelessAccessnumber) as wirelessAccessnumber ,sum(subdevicewlanradiopower) as " \
                      "subdevicewlanradiopower ,"\
                    + "sum(tcpreconnectrate) as tcpreconnectrate ,sum(httpresponesdelay) as httpresponesdelay ," \
                      "sum(dnsresponsetime) as dnsresponsetime,sum(deviceidCnt) AS deviceidCnt,"\
                    + "sum(wannumber) as wannumber,sum(wanCnt) as wanCnt,sum(subdevicenumber) as subdevicenumber," \
                      "sum(subdeviceCnt) as subdeviceCnt,"\
                    + "sum(wlanneighbor_number) as wlanneighbor_number,sum(wlanneighborCnt) as wlanneighborCnt," \
                      "sum(servicenumber) as servicenumber,sum(serviceCnt) as serviceCnt";

        sql = "SELECT %s FROM %s WHERE reportTime = %s;" % (column,tableName, begintime)
        result = DB.getSQLData(sql)
        rows = result
        totalCount = getTotalCount(tableName)
        if result == []:
            nErrorCode = 1
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")

# 4、获取对比趋势图数据，对应数据库表：HGUPeriodic_city_sum（时粒度表），HGUPeriodic_city_sum_sumDay（天粒度表）
def getHGUIndexView(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []
    condition = ''

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        endtime = request.GET.get('endTime')
        # compareType= 'day' 或者 'week' 或者 'month'
        compareType = request.GET.get('comparetype')
        timeInterval = request.GET.get('timeInterval')
        # type = 'trend' 或者 'compare'
        Type = request.GET.get('type')
        hguvendor = request.GET.get('hguVendor')
        cityid = request.GET.get('cityId')

        column = "reportTime,citycode,cityId,sum(hguCnt) as hguCnt ,sum(cpurate) as  cpurate ,sum(ramrate) as " \
                 "ramrate,sum(ponrxpower) as ponrxpower," \
                 + "sum(weaklightUsers) as weaklightUsers, sum(pppoesuccessnumber) as pppoesuccessnumber ," \
                 + "sum(wirelessAccessnumber) as wirelessAccessnumber ,sum(subdevicewlanradiopower) as " \
                   "subdevicewlanradiopower ," \
                 + "sum(tcpreconnectrate) as tcpreconnectrate ,sum(httpresponesdelay) as httpresponesdelay ," \
                   "sum(dnsresponsetime) as dnsresponsetime,sum(deviceidCnt) AS deviceidCnt," \
                 + "sum(wannumber) as wannumber,sum(wanCnt) as wanCnt,sum(subdevicenumber) as subdevicenumber," \
                   "sum(subdeviceCnt) as subdeviceCnt," \
                 + "sum(wlanneighbor_number) as wlanneighbor_number,sum(wlanneighborCnt) as wlanneighborCnt," \
                   "sum(servicenumber) as servicenumber,sum(serviceCnt) as serviceCnt";

        condition = ''
        groupBy = ''

        if int(timeInterval) == 3600:
            tableName = "HGUPeriodic_city_sum"
        elif int(timeInterval) >= 86400:
            tableName = "HGUPeriodic_city_sum_sumDay"

        if compareType == 'day':
            nbegintime = int(begintime) - 86400
            nendtime = int(endtime) - 86400
        elif compareType == 'week':
            nbegintime = int(begintime) - 86400 * 7
            nendtime = int(endtime) - 86400 * 7
        elif compareType == 'month':
            nbegintime = int(begintime) - 86400 * 30
            nendtime = int(endtime) - 86400 * 30

        if hguvendor != '':
            condition = "AND HguVendor = '%s'" %(hguvendor)
            column += 'HguVendor'

        if Type == 'trend':
            if int(cityid) != 0:
                groupBy = 'GROUP BY reportTime '
                sqlToday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s AND cityId = %s %s %s;" % (
                    column, tableName, int(begintime), int(endtime), int(cityid),condition,groupBy)
                sqlYesterday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s AND cityId = %s %s %s;" % (
                    column, tableName, nbegintime, nendtime, int(cityid),condition,groupBy)
                totalCount = getTotalCount(tableName)
                resultToday = DB.getSQLData(sqlToday)
                resultYesterday = DB.getSQLData(sqlYesterday)
                rows = {begintime: resultToday, nbegintime: resultYesterday}
                if resultToday == [] or resultYesterday == []:
                    nErrorCode = 1
            else:
                groupBy = 'GROUP BY reportTime '
                sqlToday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s %s %s;" % (
                    column, tableName, int(begintime), int(endtime),condition,groupBy)
                sqlYesterday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s %s %s;" % (
                    column, tableName, nbegintime, nendtime, condition,groupBy)
                totalCount = getTotalCount(tableName)
                resultToday = DB.getSQLData(sqlToday)
                resultYesterday = DB.getSQLData(sqlYesterday)
                rows = {begintime: resultToday, nbegintime: resultYesterday}
                if resultToday == [] or resultYesterday == []:
                    nErrorCode = 1
        elif Type == 'compare':
            if int(cityid) != 0:
                column += ',areaCode'
                groupBy = 'GROUP BY areaCode '
                sqlToday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s AND cityId = %s %s %s;" % (
                    column, tableName, int(begintime), int(endtime), int(cityid),condition ,groupBy)
                sqlYesterday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s AND cityId = %s %s %s;" % (
                    column, tableName, nbegintime, nendtime, int(cityid),condition ,groupBy)
                totalCount = getTotalCount(tableName)
                resultToday = DB.getSQLData(sqlToday)
                resultYesterday = DB.getSQLData(sqlYesterday)
                rows = {begintime: resultToday, nbegintime: resultYesterday}
                if resultToday == [] or resultYesterday == []:
                    nErrorCode = 1
            else:
                groupBy = 'GROUP BY cityId '
                sqlToday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s %s %s;" % (
                    column, tableName, int(begintime), int(endtime),condition,groupBy)
                sqlYesterday = "SELECT %s FROM %s WHERE reportTime >= %s AND reportTime <%s %s %s;" % (
                    column, tableName, nbegintime, nendtime, condition,groupBy)
                totalCount = getTotalCount(tableName)
                resultToday = DB.getSQLData(sqlToday)
                resultYesterday = DB.getSQLData(sqlYesterday)
                rows = {begintime: resultToday, nbegintime: resultYesterday}
                if resultToday == [] or resultYesterday == []:
                    nErrorCode = 1

    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")


# 5、获取质差列表数据，对应数据库表：
# (1)CPU质差：HGUPeriodic_city_CPU_bad（小时粒度）,HGUPeriodic_city_CPU_bad_sumDay(天粒度)
# (2)RAM质差：HGUPeriodic_city_RAM_bad（小时粒度）,HGUPeriodic_city_RAM_bad_sumDay(天粒粒度）
# (3)弱光占比：HGUPeriodic_city_weaklight_bad（小时粒度）,HGUPeriodic_city_weaklight_bad_sumDay(天粒粒度）
# (4)下挂WLAN信号弱：HGUPeriodic_city_wan_bad（小时粒度）,HGUPeriodic_city_wan_bad_sumDay(天粒粒度）
def getHGUQualityBadList(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []
    result1 = []
    condition = ''

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        endtime = request.GET.get('endTime')
        timeInterval = request.GET.get('timeInterval')
        hguvendor = request.GET.get('hguVendor')
        Type = request.GET.get('type')
        cityid = request.GET.get('cityId')
        start = request.GET.get('start')
        limit = request.GET.get('limit')
        tableNameHour = "HGUPeriodic_city_CPU_bad"
        tableNameDay = "HGUPeriodic_city_CPU_bad_sumDay"

        if Type == 'cpurate':
            tableNameHour = "HGUPeriodic_city_CPU_bad"
            tableNameDay = "HGUPeriodic_city_CPU_bad_sumDay"
        elif Type == 'ramrate':
            tableNameHour = "HGUPeriodic_city_RAM_bad"
            tableNameDay = "HGUPeriodic_city_RAM_bad_sumDay"
        elif Type == 'weaklight':
            tableNameHour = "HGUPeriodic_city_weaklight_bad"
            tableNameDay = "HGUPeriodic_city_weaklight_bad_sumDay"
        elif Type == 'weaksignal':
            tableNameHour = "HGUPeriodic_city_wan_bad"
            tableNameDay = "HGUPeriodic_city_wan_bad_sumDay"

        if timeInterval == '3600':
            tableName = tableNameHour
        elif timeInterval == '86400':
            tableName = tableNameDay

        if hguvendor != '':
            condition = "AND hguVendor = '%s'" % (hguvendor)
            if cityid == '0':
                sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s %s LIMIT %s,%s;" % (tableName, begintime, endtime, condition, start, limit);
                print(sql)
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s %s;" % (tableName, begintime, endtime, condition);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
            else:
                sql = "SELECT * FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s LIMIT %s,%s;" % (
                tableName, cityid, begintime, endtime, condition, start, limit);
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s;" % (
                tableName, cityid, begintime, endtime, condition);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
        else:
            if cityid == '0':
                sql = "SELECT * FROM %s WHERE reportTime >= %s AND reportTime <%s LIMIT %s,%s;" % (
                tableName, begintime, endtime, start, limit);
                print(sql)
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s;" % (
                tableName, begintime, endtime);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
            else:
                sql = "SELECT * FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s LIMIT %s,%s;" % (
                tableName, cityid, begintime, endtime, start, limit);
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s;" % (
                tableName, cityid, begintime, endtime);
                result = DB.getSQLData(sql)
                result1 = DB.getSQLData(sql1)
                rows = result
                if result == []:
                    nErrorCode = 1
    totalCount = result1[0]['cnt']
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")


# 6、获取HGU软探针安装量，对应数据库表：HGUProbeInstallationFK
def getHGUProbeInstallation(request):
    json_Dirt = {}
    nErrorCode = 0
    rows = []
    result = []

    if request.method == "GET":
        tableName = "HGUProbeInstallationFK"
        sql = "SELECT probeInstallation FROM %s;" % (tableName)
        result = DB.getSQLData(sql)
        rows = result
        if result == []:
            nErrorCode = 1
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["rows"] = rows
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")

#7.导出数据
def getHGUDataCount(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    result1 = []
    condition = ''

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        endtime = request.GET.get('endTime')
        timeInterval = request.GET.get('timeInterval')
        hguvendor = request.GET.get('hguVendor')
        Type = request.GET.get('type')
        deviceId = request.GET.get('deviceid')
        cityid = request.GET.get('cityId')
        limit = request.GET.get('limit')
        tableNameHour = ""
        tableNameDay = ""

        if Type == 'cpurate':
            tableNameHour = "HGUPeriodic_city_CPU_bad"
            tableNameDay = "HGUPeriodic_city_CPU_bad_sumDay"
        elif Type == 'ramrate':
            tableNameHour = "HGUPeriodic_city_RAM_bad"
            tableNameDay = "HGUPeriodic_city_RAM_bad_sumDay"
        elif Type == 'weaklight':
            tableNameHour = "HGUPeriodic_city_weaklight_bad"
            tableNameDay = "HGUPeriodic_city_weaklight_bad_sumDay"
        elif Type == 'weaksignal':
            tableNameHour = "HGUPeriodic_city_wan_bad"
            tableNameDay = "HGUPeriodic_city_wan_bad_sumDay"

        if deviceId != None:
            tableNameHour = "HGUPeriodic_sum"
            tableNameDay = "HGUPeriodic_sum_sumDay"
		
        if timeInterval == '3600':
            tableName = tableNameHour
        elif timeInterval == '86400':
            tableName = tableNameDay

        if hguvendor != '' and hguvendor != None:
            condition = "AND hguVendor = '%s'" % (hguvendor)
            if deviceId != '' and deviceId != None:
                condition += "AND deviceid = '%s'" % (deviceId)
            if cityid == '0':
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s %s;" % (
                tableName, begintime, endtime, condition)
                result1 = DB.getSQLData(sql1)
                if result1 == []:
                    nErrorCode = 1
            else:
                sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s;" % (
                    tableName, cityid, begintime, endtime, condition);
                result1 = DB.getSQLData(sql1)
                if result1 == []:
                    nErrorCode = 1
        else:
            if deviceId != '' and deviceId != None:
                condition = "AND deviceid = '%s'" % (deviceId)
                if cityid == '0':
                    sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s %s;" % (
                    tableName, begintime, endtime, condition)
                    result1 = DB.getSQLData(sql1)
                    if result1 == []:
                        nErrorCode = 1
                else:
                    sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s %s;" %(
                        tableName, cityid, begintime, endtime, condition);
                    result1 = DB.getSQLData(sql1)
                    if result1 == []:
                        nErrorCode = 1
            else:
                if cityid == '0':
                    sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime >= %s AND reportTime <%s;" % (
                        tableName, begintime, endtime)
                    result1 = DB.getSQLData(sql1)
                    if result1 == []:
                        nErrorCode = 1
                else:
                    sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE cityId = %s AND reportTime >= %s AND reportTime <%s;" % (
                        tableName, cityid, begintime, endtime);
                    result1 = DB.getSQLData(sql1)
                    if result1 == []:
                        nErrorCode = 1
    totalCount = result1[0]['cnt']
    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["totalQueryTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")

# 8.网关SN，所用数据表：HGUPeriodic_detail
def getGatewaySNInfo(request):
    startTime = time.time()
    json_Dirt = {}
    totalCount = 0
    nErrorCode = 0
    rows = []
    result = []
    condition = ''

    if request.method == "GET":
        begintime = request.GET.get('beginTime')
        deviceId = request.GET.get('deviceid')
        limit = request.GET.get('limit')

        tableName = "HGUPeriodic_detail"
        condition = "AND deviceid = '%s'" % (deviceId)
        sql = "SELECT detail FROM %s WHERE reportTime = %s %s LIMIT 0,%s;" % (
            tableName, begintime, condition, limit)
        print(sql)
        sql1 = "SELECT COUNT(*) AS cnt FROM %s WHERE reportTime = %s %s;" % (
            tableName, begintime, condition);
        result = DB.getSQLData(sql)
        result1 = DB.getSQLData(sql1)
    totalCount = result1[0]['cnt']
    for i in range(0,totalCount):
        j = json.loads(result[i]['detail'].replace("\'","\""))
        j['timestamp'] = '%s'%(begintime)
        rows.append(j)

    json_Dirt["errorCode"] = nErrorCode
    json_Dirt["totalCount"] = totalCount
    json_Dirt["rows"] = rows
    #a ={"rows":rows}
    #json_Dirt["data"] = a
    json_Dirt["consumingTime"] = time.time() - startTime
    return HttpResponse(json.dumps(json_Dirt), content_type="application/json")


def VixtelRest(request):
    subInterface = request.GET.get('subInterface')
    #success!
    if subInterface == 'getGatewayListInfo':
        result = getGatewayListInfo(request)
        return result
    #success!
    if subInterface == 'getGatewayDetailInfo':
        result = getGatewayDetailInfo(request)
        return result
    #success!
    if subInterface == 'getHGUIndexView':
        result = getHGUIndexView(request)
        return result
    #success!
    if subInterface == 'getHGUQualityBadList':
        result = getHGUQualityBadList(request)
        return result
    #success!
    if subInterface == 'getHGUProbeInstallation':
        result = getHGUProbeInstallation(request)
        return result
    #success!
    if subInterface == 'getHGUIndexInfo':
        result = getHGUIndexInfo(request)
        return result
    # test!
    if subInterface == 'getHGUDataCount':
        result = getHGUDataCount(request)
        return result

    
    
def Vixtel(request):
    subInterface = request.GET.get('subInterface')
    #success!
    if subInterface == 'getHGUProbeInstallation':
        result = getHGUProbeInstallation(request)
        return result
    #success!
    if subInterface == 'getHGUIndexInfo':
        result = getHGUIndexInfo(request)
        return result
    #success!
    if subInterface == 'getGatewayDetailInfo':
        result = getGatewayDetailInfo(request)
        return result
    #success!
    if subInterface == 'getGatewaySNInfo':
        result = getGatewaySNInfo(request)
        return result
    
