# Experiments done to check each feature separately
### ESP32
1. `ExampleMotor`:
   - Purpose: This code was designed to validate the motor control system.
   - Procedure: It receives throttle values ranging from -1 to 1 via the serial monitor and translates them into motor actions, including reverse movement for negative values.
   
2. `ExampleSteer`:
   - Purpose: This experiment focused on testing the steering servo's performance.
   - Procedure: The code sweeps the steering servo within a predefined steering angle range. The angle can be adjusted using the variable named **steerAngle**.

3. `MPU_and_MultiLoop`:
   - Purpose: This experiment aimed to evaluate the MPU-6050 module's gyro values and explore the functionality of the ESP32 microcontroller's free RTOS, utilizing both of its cores.
   - Procedure: The code continuously reads and prints gyro values from the MPU-6050 module at specified intervals, showcasing the utilization of the microcontroller's dual-core capabilities.

4. `SerialSteer`:
   - Purpose: This code allows fine-tuning the servo angles to calibrate the steering.
   - Procedure: With the steering assembled, upload the code. Then remove the servo head from the servo, and power up the microcontroller. Open up the serial monitor and set the angle to 90. Then connect the servo head and adjust the steering angle.

5. `Sonar5x`:
   - Purpose: This experiment focused on the ultrasonic distance sensors.
   - Procedure: The code retrieves distance values from all five sonar sensors and displays them in the serial monitor.
____

### Jetson Nano

1. `HSV_RangeFinder.py`:
   - Purpose: This code allows to easily calibrate the color ranges for the purpose of detecting the objects and lines.
   - Procedure:
     - Run the code, place an object/line in front of the camera. Four windows should open-up.
      ![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/10800b84-48a0-4e79-bc91-2c36ca83dc10)

      - Now click on the object with your mouse within the window named "original". It should create a basic mask for you. 
      ![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/5a2354e6-8daa-424b-ab5c-02d1b91debfc)

      - Use the sliders to fine tune the mask.
      ![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/4cd7cfe5-3151-4d9b-84e8-bf25f20685a6)

      - Press 's' on your keyboard to print the HSV range in the terminal. It will also ask you for a name. Give the color a name in the terminal, and the program will save the color range in a JASON file in the directory: 'Data/Colors.json'.

2. `(deprecated) camThreading.py`:
   - Purpose: This code uses two cameras (Webcam and pi camera) simultaneously using threading
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/75e8cd11-6270-4a53-b95f-83817e04003b)
      > [!NOTE]
      > We're no longer using both cameras. But this is how it can be done using multithreading.
____
These experiments were conducted separately to ensure that each component and feature operates as expected in isolation. Such a systematic approach to testing ensures that the various elements of the robot's system are thoroughly examined and verified before integration into the final design.
