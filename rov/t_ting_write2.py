# -*- coding: utf-8 -*-
import serial
import time
import ast
from my_lib import my_pwm ,my_map
import math

# ArduinoMEGAとpinで接続
#ser = serial.Serial('/dev/ttyS0', 115200)
#ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0', 115200)

print "Please turn on the power PUROPO"
print "PUROPO2"

while True:
    data = ser.readline()
    try:
        dict_serial = ast.literal_eval(data)
        dict_serial = dict_serial["puropo"]
        if(dict_serial["RV1"] == 0 and dict_serial["RV2"] == 0 and dict_serial["RV3"] == 0 and dict_serial["RV4"] == 0):
            print "T-Ting Start"
            break

    except :
        pass

file = open("LogFile/log.csv", "w")

try:
    i = 1
    while True:
        data = ser.readline()
        try:
            dict_serial = ast.literal_eval(data)
            puropo_dict = dict_serial["puropo"]
            dsr1603_dict = dict_serial["dsr1603"]
            if(puropo_dict["RV1"] == 0 and puropo_dict["RV2"] == 0 and (puropo_dict["RV3"] == -87 or  puropo_dict["RV3"] == -89) and puropo_dict["RV4"] == 0):
                my_pwm(3,0,30,30) #ch1 潜水左
                my_pwm(1,0,30,30) #ch2 潜水右
                my_pwm(4,0,30,30) #ch3 推進左
                my_pwm(2,0,30,30) #ch4 推進右
                print "T-Ting End"
                break

            file.writelines(str(dict_serial))
            file.writelines("\r\n")

            # print "puropo",
            # print dict_serial["puropo"]
            # print "dsr1603",
            # print dict_serial["dsr1603"]
            print "CelBlance",
            print dict_serial["CelBlance"]
            print "Cullent",
            print dict_serial["Cullent"]
            #print "temperature",
            #print dict_serial["temperature"]
            # print ""

            RV1 = int(puropo_dict["RV1"])
            RV2 = int(puropo_dict["RV2"])
            X9D = int(dsr1603_dict["X"])

            #プロポのRV1、RV2から角度を求める
            #(-179_0_180)
            puropo_angle = math.degrees(math.atan2(RV2,RV1))

            #(-179_0_180)→(0_360)
            if RV2 < 0:
                puropo_angle = 360 + puropo_angle

            #向いている角度によってモータの強さを変える軸を変更する
            if puropo_angle <= 45 or puropo_angle >= 315:
                strength = RV1
            elif puropo_angle <= 135:
                strength = RV2
            elif puropo_angle <= 225:
                strength = -RV1
            elif puropo_angle <= 315:
                strength = -RV2
            #End----------------------------------

            if puropo_angle > 180:
                LeftPower = -(360 - puropo_angle) + strength
                RightPower = (360 - puropo_angle) + strength
            else:
                LeftPower = puropo_angle + strength
                RightPower = -puropo_angle + strength

            #目的までの角度が近すぎると回転数が落ちるすぎるため最小限回す
            if RightPower < 25 and RightPower > -25:
                RightPower = RightPower * 3
                if RightPower > 25 or RightPower < -25:
                    if RightPower > 0:
                         RightPower = 25
                    else:
                        RightPower = -25
            if LeftPower < 25 and LeftPower > -25:
                LeftPower = LeftPower * 3
                if LeftPower > 25 or LeftPower < -25:
                    if LeftPower > 0:
                         LeftPower = 25
                    else:
                        LeftPower = -25
            #End----------------------------------

            #強さがMAXを超えないようにする
            if LeftPower > 100:
                LeftPower = 100
            elif LeftPower < -100:
                LeftPower = -100

            if RightPower > 100:
                RightPower = 100
            elif RightPower < -100:
                RightPower = -100
            #End----------------------------------

            RightPower = int(RightPower)
            LeftPower = int(LeftPower)

            print "角度 : " , puropo_angle #プロポで指示した角度
            print "強さ : " , strength #プロポで指示した強さ
            print "RightPower : " , RightPower
            print "LeftPower : " , LeftPower
            print ""

            #ch1 潜水左
            #ch2 潜水右
            #ch3 推進左
            #ch4 推進右

            #操縦モード3
            my_pwm(3,LeftPower,100,100) #推進左
            my_pwm(4,RightPower,80,80) #推進右

            i += 1
        except SyntaxError:
            print "SyntaxError Error!!"

        except :
            pass

except KeyboardInterrupt:

    ser.close()
    file.close()
    my_pwm(3,0,30,30) #ch1 潜水左
    my_pwm(1,0,30,30) #ch2 潜水右
    my_pwm(4,0,30,30) #ch3 推進左
    my_pwm(2,0,30,30) #ch4 推進右
