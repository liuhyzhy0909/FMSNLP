#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/11/20 16:27
# @Author  : zhm
# @File    : RangeTimeEnum.py
# @Software: PyCharm



# 范围时间的默认时间点
class RangeTimeEnum():
    day_break = 3  # 黎明
    early_morning = 8  # 早
    morning = 10  # 上午
    noon = 12  # 中午、午间
    afternoon = 15  # 下午、午后
    night = 18  # 晚上、傍晚
    lateNight = 20  # 晚、晚间
    midNight = 23  # 深夜
    FirstHalfYear = 1 # 上半年开始月份
    EndHalfYear = 6  # 下半年开始月份
    FirsSeason = 1  #第一季度开始月份
    SecondSeason = 4 #第二季度开始月份
    ThirdSeason = 7 #第三季度开始月份
    FourthSeason = 10 #第四季度开始月份


if __name__ == "__main__":
    print(RangeTimeEnum.afternoon)
