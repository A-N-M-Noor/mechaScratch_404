import time
import board
import adafruit_hcsr04
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.D6, echo_pin=board.D12)

while True:
    try:
        t = time.time()
        print( ( round(sonar.distance, 2), round((time.time() - t)*1000, 2) ) )
    except RuntimeError:
        print("Retrying!")
    time.sleep(0.1)
