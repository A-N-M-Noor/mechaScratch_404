# Circuitry
### Circuit Schematic:
![Schematic](https://raw.githubusercontent.com/A-N-M-Noor/mechaScratch_404/main/schematic/Schematic_Circuit-mechaScratch_404_2023-10-31.png)

### ESP32 Pinout:
![Schematic](https://raw.githubusercontent.com/A-N-M-Noor/mechaScratch_404/main/schematic/ESP32_Pins.png)

* Only one GPIO pin is used per sonar sensor.
* One GPIO pin is used to take input from a button and also to control an indicator LED.
* A buck module is used for powering up the servo motor, which is set to 6V.
* A buck module is used for powering up the ESP32.
* A buck-boost module is used to constantly supply the motors with 12V.
* A buzzer is used as an indicator.
* A USB-TTL converter is used to communicate between the Jetson and the ESP32.
