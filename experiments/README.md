# Experiments done to check each feature separately
1. `ExampleMotor`:
   - Purpose: This code was designed to validate the motor control system.
   - Procedure: It receives throttle values ranging from -1 to 1 via the serial monitor and translates them into motor actions, including reverse movement for negative values.
   
1. `ExampleSteer`:
   - Purpose: This experiment focused on testing the steering servo's performance.
   - Procedure: The code sweeps the steering servo within a predefined steering angle range. The angle can be adjusted using the variable named **steerAngle**.

1. `MPU_and_MultiLoop`:
   - Purpose: This experiment aimed to evaluate the MPU-6050 module's gyro values and explore the functionality of the ESP32 microcontroller's free RTOS, utilizing both of its cores.
   - Procedure: The code continuously reads and prints gyro values from the MPU-6050 module at specified intervals, showcasing the utilization of the microcontroller's dual-core capabilities.

1. `Sonar5x`:
   - Purpose: This experiment focused on the ultrasonic distance sensors.
   - Procedure: The code retrieves distance values from all five sonar sensors and displays them in the serial monitor, facilitating a comprehensive assessment of their functionality.

These experiments were conducted separately to ensure that each component and feature operates as expected in isolation. Such a systematic approach to testing ensures that the various elements of the robot's system are thoroughly examined and verified before integration into the final design.
