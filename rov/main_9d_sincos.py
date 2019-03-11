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

while True:
    data = ser.readline()
    try:
        dict_serial = ast.literal_eval(data)
        dict_serial = dict_serial["dsr1603"]
        print "今の9軸X座標",
        print dict_serial["X"],
        print "を維持しながら3秒進みます"
        break

    except :
        pass



i = 0
X = 0
Left = 0
Right = 0

def SpecifiedAngle(strength,angle):
    #目的地の角度―現在の角度
    RightX = math.cos(angle*math.pi/180) - math.cos(dict_serial["X"]*math.pi/180)
    #print "Right " ,RightX
    LeftX = math.sin(angle*math.pi/180) - math.sin(dict_serial["X"]*math.pi/180)
    #print "LeftX " ,LeftX

    if(angle > 180):
        Left = 50 + LeftX * 10
        Right = 50 - RightX * 10
    else:
        Left = 50 + LeftX * 10
        Right = 50 - RightX * 10


    if Left > 100:
        Left = 100
    elif Left < 0:
        Left = 0

    if Right > 100:
        Right = 100
    elif Right < 0:
        Right = 0

    print "Right " ,Right
    print "Left " ,Left

    print ""

    my_pwm(3,int(Left),100,100) #Left
    my_pwm(4,int(Right),100,100) #Right

def my_9dX(val):
    if(val >= 181 and val <= 359):
        val = val - 360
    return val

try:
    while True:
        data = ser.readline()
        try:
            dict_serial = ast.literal_eval(data)

            i += 1

            # print "puropo",
            # print dict_serial["puropo"]
            # print "dsr1603",
            # print dict_serial["dsr1603"]
            # print "CelBlance",
            # print dict_serial["CelBlance"]
            # print "Cullent",
            # print dict_serial["Cullent"]
            # print "temperature",
            # print dict_serial["temperature"]
            # print ""

            dict_serial = dict_serial["dsr1603"]

            # my_9dX(dict_serial["X"])
            # print "生データ : "
            # print dict_serial["X"]
            # print "変換 : "
            # print my_9dX(dict_serial["X"])

            #X = my_9dX(dict_serial["X"])
            print "9DX:" , dict_serial["X"]

            # RightX = abs(math.cos(dict_serial["X"]*math.pi/180))
            # print "Right " ,RightX
            #
            # LeftX = abs(math.sin(dict_serial["X"]*math.pi/180))
            # print "LeftX " ,LeftX


            SpecifiedAngle(100,180);


            # Left = 63 - X
            # Right = 60 + X
            #
            # if Left > 100:
            #     Left = 100
            # elif Left < 0:
            #     Left = 0
            #
            # if Right > 100:
            #     Right = 100
            # elif Right < 0:
            #     Right = 0

            # print "左 : ",
            # print Left,
            # print "  ",
            # print "右 : ",
            # print Right
            # print ""

            #my_pwm(3,Left,100,50) #Left
            #my_pwm(4,Right,100,50) #Right

            #推進左 M60 50 1240
            #推進右 M52 50 1254

            #推進左 M63 100 3530
            #推進右 M60 100 3540

            #推進左 M50 100  26??
            #推進右 M50 92   26??

            #if i > 20:
            #    break

        except SyntaxError:
            print "SyntaxError Error!!"

        except :
            pass

except KeyboardInterrupt:
    ser.close()
    my_pwm(3,0,30,30) #ch1 潜水左
    my_pwm(1,0,30,30) #ch2 潜水右
    my_pwm(4,0,30,30) #ch3 推進左
    my_pwm(2,0,30,30) #ch4 推進右

my_pwm(3,0,30,30) #ch1 潜水左
my_pwm(1,0,30,30) #ch2 潜水右
my_pwm(4,0,30,30) #ch3 推進左
my_pwm(2,0,30,30) #ch4 推進右
