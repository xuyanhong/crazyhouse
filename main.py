# coding=utf-8
import re
import urllib2
import collections
import datetime

import urldict

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
    f = open(".\\html\\" + date + ".html",'w')
    f.write(html)

def getOnedayNum(date):
    regnew = u"新房签约(\d+)套"
    regold = u"二手房签约(\d+)套"
    newnumre = re.compile(regnew)
    oldnumre = re.compile(regold)

    with open(".\\html\\" + date + ".html","r") as f:
        for line in f:
            line = urllib2.unquote(line).decode('utf8')
            newnumbool = re.search(newnumre,line)
            oldnumbool = re.search(oldnumre,line)
            if newnumbool !=None:
                newnumstr = newnumbool.group()
                if oldnumbool !=None:
                    oldnumstr = oldnumbool.group()
                    break
                else:
                    continue

    try:
        newnum,oldnum = newnumstr.partition(u'签约')[2].partition(u'套')[0],oldnumstr.partition(u'签约')[2].partition(u'套')[0]
    except UnboundLocalError as e:
        print date,"Did not match to the data"
        newnum,oldnum = '0','0'
    return newnum,oldnum

def main():
    ud = urldict.getUrldict()
    fr = open(".\\result\\result-" + str(datetime.date.today()) + ".txt",'a')
    for key in ud:
        try:
            getOnedayHtml(key,ud[key])
        except Exception as ex:
            print key,ex,' Did not get html'
            fr.write(key +' ' + '0 0' +  '\n' )
            continue
        newnum,oldnum = getOnedayNum(key)
        fr.write(key +' ' +  newnum + ' ' +  oldnum + '\n')
    fr.close()

if __name__ == '__main__':
    main()