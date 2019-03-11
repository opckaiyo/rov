# -*- coding: utf-8 -*-
import time
from my_lib import my_pwm , my_map
import ast

file = open("LogFile/log.csv", "r")
try:
    for i in range(len(open('LogFile/log.csv').readlines())):
        string_data = file.readline().rstrip('\r\n')
        dict_data = ast.literal_eval(string_data)
        print str(i+1) + " : ",
        print dict_data
        dict_data = dict_data["puropo"]
        RV1 = int(dict_data["RV1"])
        RV2 = int(dict_data["RV2"])
        RV3 = int(dict_data["RV3"])
        RV4 = int(dict_data["RV4"])

        my_pwm(3,dict_data["RV1"],100,50) #推進左
        #my_pwm(1,dict_data["RV2"],30,30) #潜水左
        my_pwm(4,dict_data["RV3"],80,44) #推進右
        #my_pwm(2,dict_data["RV4"],30,30) #潜水右

        time.sleep(0.125)
    file.close()
    my_pwm(3,0,30,30) #ch1 潜水左
    my_pwm(1,0,30,30) #ch2 潜水右
    my_pwm(4,0,30,30) #ch3 推進左
    my_pwm(2,0,30,30) #ch4 推進右

except KeyboardInterrupt:
    my_pwm(3,0,30,30) #ch1 潜水左
    my_pwm(1,0,30,30) #ch2 潜水右
    my_pwm(4,0,30,30) #ch3 推進左
    my_pwm(2,0,30,30) #ch4 推進右
    file.close()
