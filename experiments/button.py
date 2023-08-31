import RPi.GPIO as GPIO
from time import sleep
GPIO.setmode(GPIO.BCM)
GPIO.setup(24, GPIO.IN)                    #Button
while True:
    btn = GPIO.input(24)
