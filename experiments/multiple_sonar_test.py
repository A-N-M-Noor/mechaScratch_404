import time
import board
import adafruit_hcsr04

sonars = [
    adafruit_hcsr04.HCSR04(trigger_pin=board.D6,  echo_pin=board.D12), #Left
    adafruit_hcsr04.HCSR04(trigger_pin=board.D0,  echo_pin=board.D5),  #Front-Left
    adafruit_hcsr04.HCSR04(trigger_pin=board.D9,  echo_pin=board.D25), #Front
    adafruit_hcsr04.HCSR04(trigger_pin=board.D7,  echo_pin=board.D1),  #Front-Right
    adafruit_hcsr04.HCSR04(trigger_pin=board.D11, echo_pin=board.D8)   #Right
]

while True:
    txt = "Values"
    for i in range(5):
        try:
            dst = sonars[i].distance
            txt = txt + f" -- {dst:.2f}"
        except RuntimeError:
            txt = txt + " -- errr"
    print(txt)
    #time.sleep(0.1)
