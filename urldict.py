# coding=utf-8
import collections
import datetime


oldest = datetime.date(2013,02,01) #2013-01-08
today = datetime.date.today()


def getOneday(n, start_at=None):
    if start_at is None:
        start_at = oldest

    numday = datetime.timedelta(days=n)
    oneday = start_at + numday
    return oneday


def getUrldict(start_at=None):
    if start_at is None:
        start_at = oldest

    urldict = collections.OrderedDict()
    oneday = start_at
    n = 0
    while oneday < today:
        daynum = oneday.strftime('%Y%m%d') #20130201
        urldict[str(oneday)] = "http://www.tmsf.com/upload/report/mrhqbb/" + daynum + "/index.html"
        n += 1
        oneday = getOneday(n, start_at)
    return urldict
