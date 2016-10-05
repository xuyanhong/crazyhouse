# coding=utf-8
import collections
import datetime

startday = datetime.date(2013,02,01) #2013-01-08
today = datetime.date.today()

def getOneday(n):
    numday = datetime.timedelta(days=n)
    oneday = startday + numday
    return oneday

def getUrldict():
    urldict = collections.OrderedDict()
    oneday = startday
    n = 0
    while oneday < today:
        daynum = oneday.strftime('%Y%m%d') #20130201
        urldict[str(oneday)] = "http://www.tmsf.com/upload/report/mrhqbb/" + daynum + "/index.html"
        n += 1
        oneday = getOneday(n)
    return urldict