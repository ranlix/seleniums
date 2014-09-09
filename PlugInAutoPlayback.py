#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv
# import sys
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def PlaugIn_IE_AutoPlayback():
    """IE自动化测试plugin对于DRM streaming的播放, 并保存每一次生成的log"""
    browser = webdriver.Ie()
    browser.get('http://build.visualon.com/release/3.12.20-B70591/package/Ericsson/Plugin/Sample/window/SamplePlayer.html')
    time.sleep(30)
    elem = browser.find_element_by_id('userContext')  # Find the search box
    elem.send_keys('http://10.2.68.24/ericsson/drm/cars/cars-nodrm.m3u8' + Keys.RETURN)
    browser.find_element_by_id('userContextBtn').click()
    print 'Start to play!'
    time.sleep(30)
    browser.quit()
    time.sleep(10)
    return True


def analyzeLogs(logspath):
    now = datetime.datetime.now()
    newfolder = now.strftime('%Y%m%d-%H%M%S')
    newFolderPath = logspath + '\\' + newfolder
    if not os.path.exists(newFolderPath):
        os.mkdir(newFolderPath)
    else:
        pass

    for i in xrange(1, 5):
        print i
        flag = PlaugIn_IE_AutoPlayback()
        print flag
        if flag:
            try:
                newLogFileName = newFolderPath + "\\" + str(i) + '.log'
                print newFolderPath
                os.rename(logspath + 'volog.log', newLogFileName)
                files = os.listdir(logspath)
                print files
            except Exception as e:
                print i
                print e
        else:
            pass
    print "Logs are ready!!!"
    return newFolderPath
