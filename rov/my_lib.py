
import Adafruit_PCA9685
import RPi.GPIO as GPIO
import time
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(66)

def my_pwm(ch ,val ,maxuppwm ,maxdownpwm):
    if(val >= 0):
        val = (val - 0) * (maxuppwm - 0) / (100 - 0) + 0
        if (val + 425) < 435:
            val = 425
        else:
            val = 425 + val
        pwm.set_pwm(ch, 0, val)   #443
        #print val
    else:
        val = -val
        val = (val - 0) * (maxdownpwm - 0) / (100 - 0) + 0
        if (val - 425) > 413:
            val = 425
        else:
            val = 425 - val
        pwm.set_pwm(ch, 0, val)   #416
        #print val

def my_map(val):
    val = (val - 0) * (100 - 0) / (359 - 0) + 0
    return val
