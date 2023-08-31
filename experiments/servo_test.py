import RPi.GPIO as GPIO
import pigpio #Range: 700-2250 #Steer 1050-1750
import time 
servo = 4 
pwm = pigpio.pi() 
pwm.set_mode(servo, pigpio.OUTPUT)
pwm.set_PWM_frequency(servo, 50)
pwm.set_servo_pulsewidth(servo, 1400)
while True:
    angle = input("MICRO: ")
    pwm.set_servo_pulsewidth(servo, int(angle))
    time.sleep(1)
