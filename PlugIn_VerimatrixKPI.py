#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import re
import csv
import time
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def PlaugIn_IE_AutoPlayback():
    """IE自动化测试plugin对于DRM streaming的播放, 并保存每一次生成的log"""
    browser = webdriver.Ie()
    browser.get('http://build.visualon.com/release/3.12.20-B70591/package/Ericsson/Plugin/Sample/window/SamplePlayer.html')
    time.sleep(30)
    elem = browser.find_element_by_id('userContext')  # Find the text_input box
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
    newFolderPath = os.path.join(logspath, newfolder)
    if not os.path.exists(newFolderPath):
        os.mkdir(newFolderPath)
    else:
        pass

    for i in xrange(1, 10):
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


pattern_Open = "\d{2}:\d{2}:\d{2}\.\d{3} @@@VOLOG.*\[Open\] (call open )?@ (\d*)"
pattern_Video = "\d{2}:\d{2}:\d{2}\.\d{3} @@@VOLOG.*\[Video\] (gonna to be rendered )@ (\d*)"
pattern_Decrypt = "(\d*:\d*:\d*.\d{3}) @@@VOLOG.* VR Decrypt"

patternDic = {
    "Open": pattern_Open,
    "Video": pattern_Video,
    "Decrypt": pattern_Decrypt,
}

patternList1 = ["Open", "Video"]
patternList2 = ["Decrypt"]
patternList3 = ["Open2Video"]

patternList = patternList1 + patternList2 + patternList3


def timeshift(inputtime, outputtime):
    time1 = datetime.datetime.strptime(inputtime, '%H:%M:%S.%f')
    time2 = datetime.datetime.strptime(outputtime, '%H:%M:%S.%f')
    delta = time2 - time1
    timeshift1 = delta.microseconds / 1000 + delta.seconds * 1000
    return timeshift1


def text2list(logfile):
    """translate text segment to new dictionary: {"Stop":xx, "Close":yy..}"""
    content = open(logfile).read()
    segmentDicList = {}
    segmentList = []
    for key, vaule in patternDic.items():
        result = re.findall(vaule, content)
        if key in patternList1:  # 当关键字只能是唯一的时候
            # 如果搜寻不到，打印错误并且设置输出值为空
            try:
                segmentDicList[key] = int(result[0][-1])
            except Exception as e:
                print key
                print "ErrorInfo: ", e
                segmentDicList[key] = "NA"
        else:  # 当关键字应该出现2次的情况
            if len(result) >= 2:
                segmentDicList[key] = timeshift(result[0], result[1])
            else:
                segmentDicList[key] = "NA"
    segmentList = [segmentDicList[key] for key in patternList[:3]]
    if "NA" not in segmentList:
        if len(segmentList) == 3:  # 如果成功取到三个元素，则可以进行运算计算出花费时间
            print "Ready to caculate the time of 'open to render'"
            print segmentList
            cost = segmentList[1] - segmentList[0]
            segmentList.append(cost)
        else:
            pass
    else:
        print logfile
        print str(logfile) + "Data is not complete:("
    return segmentList


def LogsList(urlsPath):
    file_list = os.listdir(urlsPath)
    dataList = []
    for each_file in file_list:
        if each_file.endswith(".log"):
            filespath = os.path.join(urlsPath, each_file).replace("\\", "/")
            dataList.append(text2list(filespath))
        else:
            pass
    return dataList


def main():
    logspath = r'\\fs\Temp\alex\logs\\'
    if 'volog.log' in os.listdir(logspath):
        try:
            os.remove(os.path.join(logspath, 'volog.log'))
        except Exception as e:
            print e
    else:
        pass
    urlsPath = analyzeLogs(logspath)
    new_csv = os.path.join(urlsPath, r"result.csv")
    csvfile = file(new_csv, 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(patternList)
    line_list = LogsList(urlsPath)
    print line_list
    for i in line_list:
        print i
        print "____________"
        writer.writerow(i)
    csvfile.close()
    os.startfile(urlsPath)

if __name__ == '__main__':
    main()
    ipt = raw_input("Input any key to continue...")
    if ipt:
        pass
