#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/22 10:21
# @Author  : zhm
# @File    : Test.py
# @Software: PyCharm
import importlib,sys
import regex as re
import flask
import arrow
from TimeNormalizer import TimeNormalizer
import pickle
importlib.reload(sys)
#sys.setdefaultencoding('utf-8')

class TimeParse():
    def findTime(self,input_str):
        '''
        时间短语标准时间解析
        :param input_str:
        :return:
        '''
        tn = TimeNormalizer(isPreferFuture=True)
        t = []
        tn.parse(input_str)
        if (len(tn.timeToken) != 0):
            t.append(tn.timeToken[0].time.format("YYYY-MM-DD"))
        return t

    def findGsize(self,input_str):
        '''
        识别时间粒度
        :param input_str:
        :return:
        '''
        Day = u"天|日|号"
        pattern1 = re.compile(Day)

        Day_list = []
        for m in pattern1.finditer(input_str):
            Day_list.append(m.group())

        Interval_month = u"(\\d+(?=(个)?月[以之]?前))|(前\\d+(?=(个)?月[以之]?))"
        pattern2 = re.compile(Interval_month)

        Interval_month_list = []
        for m in pattern2.finditer(input_str):
            Interval_month_list.append(m.group())

        Day_sign = '日'
        Month = u"月"
        Season = u"季"
        HalfYear = u"半年"
        Year = u"年"
        Interval_month_sign = 'INM'
        Gsize = ''
        if (len(Interval_month_list) > 0):
            Gsize = Gsize + Interval_month_sign
        elif (len(Day_list) > 0):
            Gsize = Gsize + Day_sign
        elif (input_str.find(Month) > 0 and input_str.find(Day) < 0):
            Gsize = Gsize + Month
        elif (input_str.find(Season) > 0 and input_str.find(Month) < 0 and input_str.find(Day) < 0):
            Gsize = Gsize + Season
        elif (input_str.find(HalfYear) > 0 and input_str.find(Season) < 0 and input_str.find(Month) < 0 and input_str.find(Day) < 0):
            Gsize = Gsize + HalfYear
        elif (input_str.find(Year) > 0 and input_str.find(Season) < 0 and input_str.find(Month) < 0 and input_str.find(
                Day) < 0 and input_str.find(HalfYear) < 0):
            Gsize = Gsize + Year

        return Gsize


    def getEndTime(self,timestr,grandsize):
        Month = u"月"
        Season = u"季"
        HalfYear = u"半年"
        Year = u"年"
        Day = u"日"
        Interval_month_sign = 'INM'
        EndTime = ''
        timeformat = "YYYY-MM"
        if grandsize == Year:
            start = arrow.get(timestr)
            end = start.shift(months=+11)
            start = start.format(timeformat)
            end = end.format(timeformat)
            EndTime = 'begin ' + start + ' end ' + end

        elif grandsize == HalfYear:
            start = arrow.get(timestr)
            end = start.shift(months=+5)
            start = start.format(timeformat)
            end = end.format(timeformat)
            EndTime = 'begin ' + start + ' end ' + end
        elif grandsize == Season:
            start = arrow.get(timestr)
            end = start.shift(months = +2)
            start = start.format(timeformat)
            end = end.format(timeformat)
            EndTime = 'begin ' + start + ' end ' + end

        elif grandsize == Interval_month_sign:
            start = arrow.get(timestr)
            #start = start.shift(month = +1)
            end = arrow.utcnow()
            start = start.format(timeformat)
            end = end.format(timeformat)
            EndTime = 'begin ' + start + ' end ' + end

        elif grandsize == Month:
            EndTime = arrow.get(timestr).format(timeformat)

        elif grandsize == Day:
            EndTime = arrow.get(timestr).format("YYYY-MM-DD")

        return EndTime

    def getTime(self,string):#输入字符串
        pkl_file = open('timedict_re.pkl', 'rb')
        time_str = pickle.load(pkl_file)
        pkl_file.close()

        pattern = re.compile(time_str)
        # 季度暂不支持
        #string = u'朔州中心医院去年上半年门诊量。2015年3月4日门诊量。今年8月9月。今年3月门诊量。前天门诊量。本月平均住院日。这个月。今年下半年。当前季度。本季度。下个季度。上季度。第一季度平均住院日。第2季度床位使用率。上个月。当前月。上半年。1月。12月。一月。前年一月份。去年十一月份。后年12月份。2018年六月'
        #string = string.split('。')
        #string = [x for x in string if len(x) != 0]
        #print(string)
        time_list = []
        for m in pattern.finditer(string):
            #print(m.group())
            Gsize = self.findGsize(TimeParse,m.group())
            Time = self.findTime(TimeParse,m.group())
            #print(Time,Gsize)
            for t in Time:
              endT = self.getEndTime(TimeParse,t,Gsize)
              time_list.append(endT)

        #print(time_list)
        #print("------------------------")
        return  time_list

if __name__ == "__main__":
    pkl_file = open('timedict_re.pkl', 'rb')
    time_str = pickle.load(pkl_file)
    pkl_file.close()

    pattern = re.compile(time_str)
        #季度暂不支持
    string = u'中心医院前4个月住院收入'
    #。全院六七八月份手术量是多少。全院6、7、8月份检查人数是多少。心内科前6个月门诊人次。肾内科3月、6月门诊人次。中医肾内科34月份药占比'
    #string = u'肾内科3月、6月门诊人次。朔州中心医院去年上半年门诊量。朔州中心医院上一年总收入是多少。2015年3月4日门诊量。今年8月9月。今年3月门诊量。前天门诊量。本月平均住院日。这个月。今年下半年。当前季度。本季度。下个季度。上季度。第一季度平均住院日。第2季度床位使用率。上个月。当前月。上半年。1月。12月。一月。前年一月份。去年十一月份。后年12月份。2018年六月'
    string = string.split('。')
    string = [x for x in string if len(x)!=0]
    for s in string:
        time_list = []
        '''
        rule = u'[0-9]{4}(年|\\.|\\-)((01)|(02)|(03)|(04)|(05)|(06)|(07)|(08)|(09)|(10)|(11)|(12)|([1-9]))月'
        pattern = re.compile(rule)
        s = u'2017年06月内一科门诊量'
        '''
        for m in pattern.finditer(s):
            #ss = m.group()
            print(m.group())
            Gsize = TimeParse.findGsize(TimeParse,m.group())
            #print(Gsize)
            Time = TimeParse.findTime(TimeParse,m.group())
            #print(Time,Gsize)
            for t in Time:
                endT = TimeParse.getEndTime(TimeParse,t, Gsize)
                time_list.append(endT)
        # Gsize = findGsize(s)#在匹配后的时间字符串内寻找代表时间粒度的关键字，目的是排查除时间表达式之外的字符串含有相应的关键字
        print(time_list)
        print("------------------------")
