# -*- coding: utf-8 -*-
import serial
import time
import ast
from my_lib import my_pwm ,my_map

# ArduinoMEGAとpinで接続
#ser = serial.Serial('/dev/ttyS0', 115200)
#ArduinoMEGAとUSBケーブル接続
ser = serial.Serial('/dev/ttyACM0', 115200)

print "Please turn on the power PUROPO"

#プロポ初期セットアップ処理：プロポを左右のレバーを0にセットでデータどりスタートする
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

#初期処理が完了を確認後データどり用のファイルを開き準備する
file = open("LogFile/log.csv", "w")

#データどり開始
#データをはシリアル通信でArduinoから送られてくる。Arduinoでタイミングを設定する
try:
    i = 1
    while True:
        data = ser.readline()
        try:
            dict_serial = ast.literal_eval(data)
            puropo_dict = dict_serial["puropo"]
            if(puropo_dict["RV1"] == 0 and puropo_dict["RV2"] == 0 and (puropo_dict["RV3"] == -87 or  puropo_dict["RV3"] == -89) and puropo_dict["RV4"] == 0):
                my_pwm(3,0,30,30) #ch1 潜水左
                my_pwm(1,0,30,30) #ch2 潜水右
                my_pwm(4,0,30,30) #ch3 推進左
                my_pwm(2,0,30,30) #ch4 推進右
                print "T-Ting End"
                break

            #データ記録
            file.writelines(str(dict_serial))
            file.writelines("\r\n")

            #受信データ表示
            print "puropo",
            print dict_serial["puropo"]
            print "dsr1603",
            print dict_serial["dsr1603"]
            print "CelBlance",
            print dict_serial["CelBlance"]
            print "Cullent",
            print dict_serial["Cullent"]
            print "temperature",
            print dict_serial["temperature"]
            print ""

            dict_serial = dict_serial["puropo"]

            #ch1 潜水左
            #ch2 潜水右
            #ch3 推進左
            #ch4 推進右

            #操縦モード１
            my_pwm(3,dict_serial["RV1"],100,100) #推進左 5860
            my_pwm(1,dict_serial["RV2"],100,100) #潜水左 7880
            my_pwm(4,dict_serial["RV3"],100,100) #推進右 6120
            my_pwm(2,dict_serial["RV4"],100,100) #潜水右

            #操縦モード2
            #my_pwm(3,dict_serial["RV1"]  + my_map(dict_serial["RV2"]),100,100) #推進左
            #my_pwm(1,dict_serial["RV4"],100,100) #潜水左
            #my_pwm(4,dict_serial["RV1"] - my_map(dict_serial["RV2"]),100,100) #推進右
            #my_pwm(2,dict_serial["RV4"],100,100) #潜水右

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
