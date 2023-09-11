import RPi.GPIO as GPIO
import time

PWMA = 22
AIN1 = 17
AIN2 = 27
STBY = 23
dc = 95 # duty cycle (0-100) for PWM pin

# Pin Setup:
GPIO.setmode(GPIO.BCM)
GPIO.setup(PWMA, GPIO.OUT)
GPIO.setup(AIN1, GPIO.OUT)
GPIO.setup(AIN2, GPIO.OUT)
GPIO.setup(STBY, GPIO.OUT)
pwm = GPIO.PWM(PWMA, 50)  # Initialize PWM on pwmPin 50Hz frequency

GPIO.output(STBY, GPIO.HIGH)
GPIO.output(AIN1, GPIO.LOW)
GPIO.output(AIN2, GPIO.HIGH)
pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    while True:
        cycle = int(input("Duty cycle: "))
        pwm.ChangeDutyCycle(cycle)
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    GPIO.output(STBY, GPIO.LOW)
    pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO
