# -*- coding:utf-8 -*-
__author__ = 'rwang'

import urllib2
import urllib
import re
import os
import time
import sendmail
import configuration
import logging
import logging.config
import socket
socket.setdefaulttimeout(10.0)

#pip install BeautifulSoup
#from BeautifulSoup import BeautifulSoup
from bs4 import *
#global save_folder, original_folder
#__RETRY_TIMES__ = 3
#__MONITOR_WAITING__ = 60*60*4

class qiang:
    def __init__(self):
        logging.config.fileConfig("logging.ini")
        self.__logger = logging.getLogger('qiang')
        self.__c = configuration.configuration()
        self.__c.fileConfig("configuration.ini")
        self.__RETRY_TIMES__ = int(self.__c.getValue("Runtime","retry_times"))

    def __gethrefname(self, content, kw):
        title = ""
        contents = content.split(kw)
        if len(contents) > 1:
            cutoff = contents[1].split("</a>")[0].split(">")
            if len(cutoff) > 1:
                title = cutoff[1]
        #print "To strip all blank"
        while True: #strip all blank
            if title == title.strip():
                break
            else:
                title = title.strip()
        #print "strip done"
        #print title
        return title

    def __genBaseUrl(self, url):
        return url.split("/")[0] + "//" + url.split("/")[2] + "/"
        #baseurl = url.strip(url.split("/")[len(url.split("/"))-1])

    def __RetrievePageData(self, url):
        data = ""
        nRetry = False
        for i in range(0, self.__RETRY_TIMES__):
            #print "to visit url %s" %url
            if nRetry:
                self.__logger.warn("Retry %i" %i)
            data = self.__getHtmlData(url)
            if data != "":
                break
            else:
                nRetry = True
        return data

    def __getHtmlData(self, url):
        data = ""
        req = urllib2.Request(url)
        try:
            u = urllib2.urlopen(req)
            data = u.read()
            #data = u.read().decode('utf-8')
        except urllib2.URLError, e:
            self.__logger.error(e.reason)
        finally:
            return data
    '''
    def __getHtmlData1(self, url):
        data = ""
        try:
            u = urllib.urlopen(url)
            data = u.read().decode('utf-8')
        except urllib2.URLError, e:
            self.__logger.error(e.reason)
        finally:
            return data
    '''
    def __dynamic_dict(self,datalist):
        d = {}
        for data in datalist:
            key = data.split("=")[0]
            value = data.split("=")[1]
            d[key] = value
        #print d
        return d

    def __retrievePages(self, url,keyword):
        #data = urllib.urlopen(url).read().decode('utf-8')
        data = self.__RetrievePageData(url)
        if data == "":
            return False
        soup = BeautifulSoup(data,"html.parser")
        #print keyword
        overs = soup.find_all('li',attrs=self.__dynamic_dict(keyword.split(",")))
        #print overs
        if overs != []:
            return False

        #陈粒小梦大半2016巡回演唱会—天津站" p="18359
        for over in overs:
            print "===",over,"==="
        #print "__retrievePages is true"
        return True

        '''
        urllist = []
        html,content = self.__getahref(url)
        #print html
        print content
        return True

        if html == "":
            return []
        pat = re.compile(r'href="([^"]*)"')
        pat2 = re.compile(r'http')
        baseurl = self.__genBaseUrl(url)

        for item in content:
            h = pat.search(str(item))
            if h is None:
                continue
            href = h.group(1)
            name = self.__gethrefname(html, href)
            #print href,name

            if (name.find(keyword) != -1):
                if pat2.search(href):
                    ans = href
                else:
                    ans = baseurl+href
                urllist.append(name+","+ans)
        if urllist != []:
            return True
        else:
            return False
        '''
    def __sendReport(self,mailbody=""):
        srv = self.__c.getValue("Report","smtpserver")
        port = self.__c.getValue("Report","port")
        sender = self.__c.getValue("Report","sender")
        fromname = self.__c.getValue("Report","from")
        subject = self.__c.getValue("Report","subject")
        pwd = self.__c.getValue("Report","password")
        to = self.__c.getValue("Report","to")
        #attachments = None
        #mode = self.__c.getValue("Project","mode")
        sendmail.sendmail(srv, port, sender, subject, fromname, pwd, to, "", mailbody)

    def __genMessage(self, data):
        body_prefix = '<!DOCTYPE html><html><head lang="en"><meta charset="UTF-8"><title></title></head><body>'
        body_suffix = '</body></html>'
        return body_prefix + data + body_suffix

    def __refreshInterval(self):
        return int(self.__c.getValue("Runtime","interval"))

    def __beContinue(self):
        if self.__c.getValue("Runtime","continue").lower() == "no":
            return False
        else:
            return True

    def monitor(self, checklist):
        #urllist, mainkw):
        while True:
            interval = self.__refreshInterval()
            url_count = len(checklist)
            remove_count = 0
            for i in range(0,url_count):

                j = i - remove_count
                #print "j is %i" %j
                url = checklist[j][0]
                kw = checklist[j][1]
                if self.__retrievePages(url,kw) is not True:
                    self.__logger.info("Oops~ In url %s, the %s is unavailable" % (url,kw))
                    continue
                else:
                    self.__logger.info("Bingo!In url %s, the %s is available!!!" %(url,kw))
                    del checklist[j]
                    remove_count = remove_count + 1

                self.__logger.info ("Generate url notification")
                notify = '<a href=\"' + url + '\">' + url + '</a>'

                mailbody = self.__genMessage(notify)
                self.__logger.info("Send mail with notify %s" %notify)
                #self.__sendReport(mailbody)
                self.__logger.info("Send mail done")
                if len(checklist) == 0:
                    self.__logger.info("===Complete all of url monitoring, Lucky!===")
                    break
            self.__logger.info("====Finish this session of scanning pages ====")

            #break
            if self.__beContinue() is not True:
                self.__logger.info("====Time is up, quit====")
                break
            else:
                self.__logger.info("Waiting %i mins for next scan" % (interval/60))
                time.sleep(interval)


#nohup python -u qiang.py > nohup.out 2>&1 &