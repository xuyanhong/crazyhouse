# coding=utf-8
import re
import urllib2
import collections
import datetime

import urldict
import influx


def getOnedayHtml(date,url):
    send_headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36',
        'Host': 'www.tmsf.com',
        'Accept': '*/*',
    }
    req = urllib2.Request(url,headers=send_headers)
    page = urllib2.urlopen(req)
    if page.getcode() != 200:
        # maybe 404/403
        msg = "[ERROR] %s %s" % (date, page.getcode())
        raise Exception(msg)
    html = page.read()
    return html


def getOnedayNum(date, html):
    regnew = u"新房签约(\d+)套"
    regold = u"二手房签约(\d+)套"
    newnumre = re.compile(regnew)
    oldnumre = re.compile(regold)

    html = urllib2.unquote(html).decode('utf8')
    newnumbool = re.search(newnumre, html)
    oldnumbool = re.search(oldnumre, html)

    if newnumbool != None:
        newnumstr = newnumbool.group()

    if oldnumbool != None:
        oldnumstr = oldnumbool.group()

    try:
        newnum = newnumstr.partition(u'签约')[2].partition(u'套')[0]
        oldnum = oldnumstr.partition(u'签约')[2].partition(u'套')[0]
    except UnboundLocalError as e:
        print date,"Did not match to the data"
        newnum, oldnum = '0','0'
    return int(newnum), int(oldnum)


def main():
    start_at = influx.get_latest_time()
    ud = urldict.getUrldict(start_at.date())
    for key in ud:
        try:
            html = getOnedayHtml(key, ud[key])
        except Exception as ex:
            html = ''
        newnum, oldnum = getOnedayNum(key, html)
        print key, newnum, oldnum
        influx.insert(key, newnum, oldnum)


if __name__ == '__main__':
    main()
