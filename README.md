# wro_fe_2023 Engineering Documentation 
## Team Members:
* A. N. M. Noor - email: nafis.noor.202012@gmail.com
* Mahir Tajwar Chowdhury - email: tajwar185@gmail.com

## Overview of our Repository
 * `models` - the 3D printable files used in our robot.
 * `schematic` - contains the schematic of the electrical system of our robot.
 * `src` - contains the main code of our robot.
 * `experiments` - codes that were used to do experiments.
 * `video` - contains the video link of youtube where our robot can be seen in action.
 * `t-photos` - contains one serious and one funny photo of our team.
 * `v-photos` - contains the photos of the robot from all required directions
 * `others` - other essential photos

# Program infrastructure and explanation of algorithm.
### Qualifying Round
**Avoiding walls:**
The program initiates with an initial throttle value of 1 (Full forward) and a steer value of 0 (No steering). Then it evaluates each sensor, checking whether its measured distance falls below its designated maximum distance threshold. If this condition is met, the sensor's value is remapped within a range specified by a minimum and maximum value, both of which are confined to the 0-1 range. This remapping process is inversely related to distance; the closer an object is, the higher the remapped value becomes.

For sensors positioned to the sides, this recalibrated value is then either added or subtracted from the existing steer value, effectively influencing the robot's lateral movement.

In the case of the front sensor, its remapped value is employed to diminish the throttle value, effectively slowing the robot down as objects come closer. Additionally, it amplifies the current steer value, causing the robot to respond more rapidly and make sharper turns when objects are detected in close proximity.

This comprehensive sensor-driven control scheme ensures that the robot can effectively navigate and respond to its environment, making it capable of avoiding obstacles and adjusting its course as needed.

**Lap count:**
The program monitors the robot's orientation using an MPU6050 sensor and continually compares the difference in angle with the previously recorded angle. Each time this angle difference reaches close to 90 degrees, the program increments a turn count by 1 and updates the stored angle data. To achieve the goal of completing three laps, the robot must complete 12 turns in total.
Therefore, when the turn count reaches the value of 12, the program triggers the robot to operate under normal conditions for a predetermined duration. After that, the robot comes to a halt, having successfully completed three laps.

The robot harnesses the processing power of both cores of the ESP32 microcontroller by using FreeRTOS, a real-time operating system. The primary core handles all logical operations and calculations, ensuring the swift execution of tasks. Simultaneously, a separate core is dedicated to acquiring sensor data, allowing for rapid data retrieval. This dual-core configuration enables the robot to perform calculations and make decisions with remarkable speed and efficiency.

In order to achieve the highest possible efficiency and reliability, we have spent several hundred hours researching and developing the parts. The following paragraphs provide detailed information about electrical systems design.

### Parts list
* Esp32 Development Board
* 300 rpm 25GA 12V DC Gear Motor
* MG91 Servo
* Huskylens: Embedded Vision Sensor
* 5xHC-SR04 Ultrasonic Sensors
* TB6612FNG Motor Driver
* MPU6050
* 3.0 USB Type-C Buck Boost module
* XL6009 Buck Boost Module
* 3S LiPo battery input through XT60 Connector

## Mechanical Design
We've made our robot totally from scratch. Most of the parts of our robot are 3D printed, starting from chasis, wheels and so on.

### Design Decisions
* We've designed a sonar mount which is mounted at the front and the side of the robot where the front-left and front-right sonar sensors are mounted at an angle of 52.5 degree. Based on our testing, this is the optimal angle for the sonars to detect walls ahead of time, giving the bot enough time to react.
* We're using the Huskylens which is an embedded machine vision sensor based on Kendryte K210 that can recognize and track colors and objects in real-time. We're using I2C to receive tracked color position data.
* The front axle is being articulated by the Servo Motor.
* To control our Motor we have used TB6612FNG motor driver.
* MPU6050 was used to measure the real-time orientation of the robot and to count laps.
* 2 Buck-Boost modules were used. One is used for getting a constant output of 12V for the Motor and the other one is used for getting a constant 5V for esp32, HuskyLens and also the Servo.
* We used Ackerman steering as it is a vital steering geometry concept that enhances the handling and cornering performance of vehicles, making them safer and more efficient on the road. Ackerman steering, also known as Ackerman geometry or Ackerman principle, is a steering mechanism which is used in vehicles in order to enable proper turning of the wheels while maintaining optimal geometry and minimizing tire scrubbing during turns. It is commonly used in most modern vehicles, including cars, trucks, and other wheeled vehicles.
The fundamental idea behind Ackerman steering is that the inner and outer wheels of a vehicle must follow different turning radii during a turn, considering the varying angles of the front wheels. When a vehicle turns, the inner wheel needs to negotiate a tighter radius than the outer wheel to maintain a smooth turn without dragging or scuffing the tires. The Ackerman steering mechanism achieves this by using a steering linkage that connects the wheels. Typically, it consists of two tie rods connected to the steering arms on each wheel. The tie rods are connected to a central steering mechanism, such as a steering rack or a pitman arm, which is controlled by the driver. As the driver turns the steering wheel, the steering mechanism transfers the motion to the tie rods, causing the wheels to rotate accordingly. The geometry of the Ackerman steering mechanism ensures that the inner wheel turns at a sharper angle compared to the outer wheel, allowing both wheels to trace their respective turning radii accurately. By implementing Ackerman steering, vehicles can achieve better maneuverability, stability, and reduced tire wear during turns. It ensures that all wheels maintain proper contact with the road surface and minimizes the likelihood of skidding or slipping during turns.
![image](https://github.com/Ahnaf-nub/Mecha-404/assets/76505613/5aab9af5-65b7-4ce1-a794-1a9a6564b4d6)

