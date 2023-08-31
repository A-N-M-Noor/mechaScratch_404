import time
import board
import adafruit_hcsr04

import RPi.GPIO as GPIO
import pigpio

sonars = [
    adafruit_hcsr04.HCSR04(trigger_pin=board.D6,  echo_pin=board.D12), #Left
    adafruit_hcsr04.HCSR04(trigger_pin=board.D0,  echo_pin=board.D5),  #Front-Left
    adafruit_hcsr04.HCSR04(trigger_pin=board.D9,  echo_pin=board.D25), #Front
    adafruit_hcsr04.HCSR04(trigger_pin=board.D7,  echo_pin=board.D1),  #Front-Right
    adafruit_hcsr04.HCSR04(trigger_pin=board.D11, echo_pin=board.D8)   #Right
]


PWMA = 22
AIN1 = 17
AIN2 = 27
STBY = 23
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)
pwmMot = GPIO.PWM(PWMA, 50)


GPIO.output(STBY, GPIO.HIGH)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.LOW)
pwmMot.start(0)

servo = 4 #Range: #Steer 1050-1750
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)
pwm.set_servo_pulsewidth(servo, 1400)

throttle = 1
steer = 0
#        L  FL  F  FR  R
dists = [0, 00, 0, 00, 0]
#       Side    Angular   Front
rD = ( (2, 80), (2, 60), (2, 30) ) #Distance Ranges

def remap(val, old, new):
    return (new[1] - new[0])*(val - old[0]) / (old[1] - old[0]) + new[0]

def clamp(val, mini, maxi):
    if(val < mini):
        return mini
    if(val > maxi):
        return maxi
    return val

def remapC(val, old, new):
    return clamp(remap(val, old, new) , new[0], new[1])


def getThrSteerSonar(_dists):
    _thr = 1
    _steer = 0
    if(_dists[0] < rD[0][1]):
        _steer -= remapC(_dists[0], rD[0], (0.8, 0))
    if(_dists[1] < rD[1][1]):
        _steer -= remapC(_dists[1], rD[1], (1, 0))
        _thr -= remapC(_dists[1], rD[1], (0.75, 0))
        
    if(_dists[2] < rD[2][1]):
        _thr -= remapC(_dists[2], rD[2], (1, 0))
        
    if(_dists[3] < rD[1][1]):
        _steer += remapC(_dists[3], rD[1], (1, 0))
        _thr -= remapC(_dists[3], rD[1], (0.75, 0))
    if(_dists[4] < rD[0][1]):
        _steer += remapC(_dists[4], rD[0], (0.8, 0))
    
    return _thr, _steer

while True:
    for i in range(5):
        try:
            dists[i] = sonars[i].distance
        except RuntimeError:
            print(f"Sonar {i+1} not working!")
    print(dists)
    throttle, steer = getThrSteerSonar(dists)
    print(steer)
    pwm.set_servo_pulsewidth( servo, int( remap(steer, (-1,1), (1150, 1650)) ) )
    
    if(throttle >= 0):
        GPIO.output(AIN1, GPIO.LOW)
        GPIO.output(AIN2, GPIO.HIGH)
        pwmMot.ChangeDutyCycle(throttle * 100)
    else:
        GPIO.output(AIN1, GPIO.HIGH)
        GPIO.output(AIN2, GPIO.LOW)
        pwmMot.ChangeDutyCycle(-throttle * 100)
