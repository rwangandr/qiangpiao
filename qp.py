__author__ = 'rwang'
import qiang
import configuration
import logging
import logging.config
import os

if __name__ == '__main__':
    os.system("rm -rf qiang.log")
    logging.config.fileConfig("logging.ini")
    logger = logging.getLogger('main')
    q = qiang.qiang()
    c = configuration.configuration()
    c.fileConfig("configuration.ini")
    count = c.getValue("Parameters","count")
    checklist = []
    for i in range(1, int(count)+1):
        key_entry = "entry" + str(i)
        key_keyword = "keyword" + str(i)
        url = c.getValue("Parameters",key_entry)
        keyword = c.getValue("Parameters",key_keyword)
        check = [url,keyword]
        checklist.append(check)
    #print checklist
    '''
    urls = c.getValue("Parameters","entry")
    keyword = c.getValue("Parameters","keyword").split(",")
    type = c.getValue("Project","type")
    '''
    logger.info("Monitor the website with keyword %s" %(checklist))
    q.monitor(checklist)
