import RPi.GPIO as gpio
import time
from datetime import datetime
gpio.setwarnings(False)

m_trig =31
m_echo=32

m_l_trig = 7
m_l_echo=18

m_r_trig =29
m_r_echo=12

l_trig = 22
l_echo = 33

r_trig = 36
r_echo = 37

forward_left_pin = 16
reverse_left_pin = 11

forward_right_pin = 15
reverse_right_pin = 13


def delay(tf=0.00001):
    time.sleep(tf)


# ######## Distance ######## #
def fDistance(echo, trigger):
    try:        
        start = 0
        end = 0
        tl = 0
        
        gpio.cleanup()
        gpio.setmode(gpio.BOARD)
        gpio.setup(trigger, gpio.OUT)
        gpio.setup(echo, gpio.IN)
        
        gpio.output(trigger, 0)
#        delay(0.003)
        delay(0.0005)
        gpio.output(trigger, 1)
        delay()
        gpio.output(trigger, 0)
        
        while gpio.input(echo) == 0:
            start = time.time()

        while gpio.input(echo) == 1:
            end = time.time()

        if start > 0 and end > 0:
            tl = end-start
        else:
            fDistance(echo, trigger)
            
        distance = (tl*(17150+0.303*22))
#        distance+= 0.303*21
        delay(0.0005)
        gpio.cleanup()
        
#        print(distance)
        return distance
    except Exception as e:
        print(e)
        gpio.cleanup()
        fDistance(echo, trigger)
        
    
# ######### Forward Sensors ######### #
def f_sensor():
    f1 = m_sensor()
    time.sleep(0.01)
    f2 = m_r_sensor()
    time.sleep(0.01)
    f3 = m_l_sensor()
    time.sleep(0.01)
    print("m: ", f1, "r: ", f2, "l: ", f3)
    count = 0
    
    if abs(round(f1-f2, 1)) <= 1:
        if abs(round(f1-f3, 1)) <= 1:
            print("m: ", f1, "r: ", f2, "l: ", f3)
            return True
        else:
            for i in range(3):
                f3 = m_l_sensor()
                if abs(round(f1-f3, 1)) <= 1:
                    count += 1
                    if count > 1:
                        count = 0
                        print("m: ", f1, "r: ", f2, "l: ", f3)
                        return True
    
    elif abs(round(f1-f3, 1)) <= 1:
        if abs(round(f1-f2, 1)) <= 1:
            return True
        else:
            for i in range(3):
                f2 = m_r_sensor()
                if abs(round(f1-f2, 1)) <= 1:
                    count += 1
                    if count > 1:
                        count = 0
                        print("m: ", f1, "r: ", f2, "l: ", f3)
                        return True
    
    elif abs(round(f3-f2, 1)) <= 1:
        if abs(round(f1-f3, 1)) <= 1:
            return True
        else:
            for i in range(3):
                f1 = m_sensor()
                if abs(f1-f3) <= 1:
                    count += 1
                    if count > 1:
                        count = 0
                        print("m: ", f1, "r: ", f2, "l: ", f3)
                        return True
                    
    return False


# ######## Middle Forward Sensor ######## #
def m_sensor():
#    print("in m_sensor")
    distance = 0
    temp = 0
    count = 0
    while count == 0:
        for i in range(5):
            temp = fDistance(m_echo, m_trig)
#            time.sleep(0.003)
            if temp > 0:
                distance += temp
                count += 1
#        print( 'F: ',distance/count)
                    
#    if distance/count>90:
#        return 95          
    return round(distance/count, 1)


# ######## Middle Left Sensor ######## #
def m_l_sensor():
#    print(" in m_l_sensor")
    distance = 0
    temp = 0
    count = 0
    while count == 0:
        for i in range(5):
            temp = fDistance(m_l_echo, m_l_trig)
#            time.sleep(0.003)
            if temp > 0:
                distance += temp
                count += 1
#        print( 'L: ',distance/count)
                    
#    if distance/count>90:
#        return 95               
    return round(distance/count, 1)


# ######## Middle Right Sensor ######## #
def m_r_sensor():
#    print("In m_r_sensor")
    distance = 0
    temp = 0
    count = 0
    while count == 0:
        for i in range(5):
            temp = fDistance(m_r_echo, m_r_trig)
#            time.sleep(0.003)
            if temp > 0:
                distance += temp
                count += 1
#        print( 'R: ',distance/count)
        
#    if distance/count>90:
#        return 95             
    return round(distance/count, 1)


# ########  Left Sensor ######## #
def l_sensor():
#    print("In l_sensor")
    distance = 0
    temp = 0
    count = 0
    while count == 0:
        for i in range(5):
            temp = fDistance(l_echo, l_trig)
#            time.sleep(0.003)
            if temp > 0:
                distance += temp
                count += 1
#    print("Left:",round(distance/count))                
    return round(distance/count)


# ########  Right Sensor ######## #
def r_sensor():
#    print("int r_sensor")
    distance = 0
    temp = 0
    count = 0
    while count == 0:
        for i in range(5):
            temp = fDistance(r_echo, r_trig)
#            time.sleep(0.003)
            if temp > 0:
                distance += temp
                count += 1
#    print("Right:",round(distance/count))
    return round(distance/count)


#f_sensor()
#print("f_mid",round(m_sensor()))
#time.sleep(1)
#print("f_right",round(m_r_sensor()))
#time.sleep(1)
#print("f_left",round(m_l_sensor()))
#print("Left: ", l_sensor())
#print("Right: ", r_sensor())

#f