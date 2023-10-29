# wro_fe_2023 Engineering Documentation / Team mechaScratch_404
![mecha scratch main](https://github.com/A-N-M-Noor/mechaScratch_404/assets/136412241/82dec0fd-90a3-4080-8b9e-d6446caba096)

## Team Members:
> A. N. M. Noor - email: noornoorrohan15@gmail.com
 
> Mahir Tajwar Chowdhury - email: tajwar185@gmail.com


## Overview of our Repository
 * `chassis` - this folder contains the pictures of the chassis that we used on our robot.
 * `experiments` - codes that were used to do experiments.  
 * `models` - the 3D printable files used in our robot.
 * `pre` - getting started guide.
 * `schematic` - contains the schematic of the electrical system of our robot.
 * `src` - contains the main code of our robot.
 * `video` - contains the video link of YouTube where our robot can be seen in action.
 * `t-photos` - contains one serious and one funny photo of our team.
 * `v-photos` - contains the photos of the robot from all required directions
 * `others` - other essential photos.

## Program infrastructure and explanation of algorithm.

### Qualifying Round
#### Avoiding walls:
The program initiates with an initial throttle value of 1 (Full forward) and a steer value of 0 (No steering). Then it evaluates each sensor, checking whether its measured distance falls below its designated maximum distance threshold. If this condition is met, the sensor's value is remapped within a range specified by a minimum and maximum value, both of which are confined to the 0-1 range. This remapping process is inversely related to distance; the closer an object is, the higher the remapped value becomes.

For sensors positioned to the sides, this recalibrated value is then either added or subtracted from the existing steer value, effectively influencing the robot's lateral movement.

In the case of the front sensor, its remapped value is employed to diminish the throttle value, effectively slowing the robot down as objects come closer. Additionally, it amplifies the current steer value, causing the robot to respond more rapidly and make sharper turns when objects are detected in close proximity.

This comprehensive sensor-driven control scheme ensures that the robot can effectively navigate and respond to its environment, making it capable of avoiding obstacles and adjusting its course as needed.

#### Lap count:
The Jetson Nano constantly looks for the corner lines using the rear camera. Whenever it sees an orange and a blue line, it sends the data to the ESP32 and increases the turn count by one. To achieve the goal of completing three laps, the robot must complete 12 turns in total.
Therefore, when the turn count reaches the value of 12, the program triggers the robot to operate under normal conditions for a predetermined duration. After that, the robot comes to a halt, having successfully completed three laps.

The robot harnesses the processing power of both cores of the ESP32 microcontroller by using FreeRTOS, a real-time operating system. The primary core handles all logical operations and calculations, ensuring the swift execution of tasks. Simultaneously, a separate core is dedicated to acquiring sensor data, allowing for rapid data retrieval. This dual-core configuration enables the robot to perform calculations and make decisions with remarkable speed and efficiency.

### Obstacle Round
At present, the robot uses OpenCV for detecting red and green towers. The Jetson Nano detects the colors of these towers, and by utilizing the on-screen width value of the detected towers in pixels, the robot can estimate the distance to any visible tower. This estimation is based on an inverse proportional relationship, expressed by the equation:

    distance = k/width

The value of ‘k’ was determined by plotting real-life data on a graph.
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/a00f20ec-0540-41f9-9b10-cbe79204a923)

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/d5fe1201-4117-4909-a40a-e25a78df4304)

In our case, the value of ‘k’ is 2141. Using this value in the equation roughly matches the real-life data acquired from experiments.


#### Avoiding walls:
This is done the same way as in the [qualifying round](https://github.com/A-N-M-Noor/mechaScratch_404/tree/main#avoiding-walls).

#### Avoiding towers:
After obtaining the initial steer and throttle values from the sonar sensors, the program proceeds to adjust these values based on the presence of red and green towers in the environment.

The program systematically evaluates all visible towers and selects the one closest to the robot. It then examines two key factors: the distance to the target tower and its horizontal position on the screen.

* **Distance Factor:** A numeric value between 0 and 1 is generated, and this value is directly proportional to the tower's proximity to the robot. The closer the tower, the larger this value becomes.

* **Horizontal Position Factor:** Another value ranging from 0 to 1 is determined based on the tower's horizontal position on the screen. For red towers, the program aims to make right turns, so a higher value is assigned when the tower is on the right side of the screen (influencing steering significantly), and the value decreases as the tower moves towards the left side. Conversely, for green towers, the same principle applies but with reversed sides.

These two calculated values are then multiplied together, yielding a new value also ranging from 0 to 1. This new value is added to or subtracted from the existing steer value. This dynamic adjustment based on tower presence and location allows the robot to navigate and react to the positions of red and green towers, facilitating precise and adaptable movement.


#### Avoiding collisions:
To address the possibility of collisions with walls or towers after modifying the steer and throttle values using the tower detection algorithm, the program implements continuous monitoring of distance values. If any of these values fall below a specified threshold, the program overrides the modifications made by the tower-avoidance algorithm and reverts to actions based on the distance values alone.

Additionally, if any object, such as a wall or tower, approaches closer to the robot than a predefined distance threshold, the program initiates a brief backward movement. During this backward motion, the program also adjusts the steer value based on the color of the target tower. For instance, if the robot detects a red tower, it may steer left while moving backward, and for a green tower, it may steer right. This dynamic response mechanism ensures that the robot takes evasive action to avoid collisions while considering the type and location of the detected objects.


#### Lap count:
This is done the same way as in the [qualifying round](https://github.com/A-N-M-Noor/mechaScratch_404/tree/main#lap-count).

#### U-turn:
After completing the second lap, which corresponds to the 8th turn, the program saves the type of the last detected object. If this last object is determined to be red, the robot does a full 180-degree turn, accomplished through the MPU, reversing its orientation. Following this 180-degree turn, the robot resumes its normal operation, continuing with its regular navigation and obstacle avoidance methods.

Once again, the ESP32's primary core handles the calculations and decision-making processes, while the secondary core is responsible for collecting data from the distance sensors and the Jetson Nano. This configuration enables the robot to react quickly and avoid collisions with walls or obstacles.

## Electrical design of our robot.
In order to achieve the highest possible efficiency and reliability, we have spent several hundred hours researching and developing the parts. The following paragraphs provide detailed information about electrical systems design.

### Electronics Parts list
* Jetson Nano Developer Kit (4GB)
* Esp32 Development Board
* USB to TTL Serial Converter
* Micropack MWB-15 Pro FHD 2MP Stream Webcam
* Raspberry Pi Camera Module v2.1
* 500 rpm 25GA 12V DC Gear Motor
* DS3235 Servo
* 5xHC-SR04 Ultrasonic Sensors
* TB6612FNG Motor Driver
* MPU6050
* 3.0 USB Type-C Buck module
* XL6009 Buck Boost Module
* 3S LiPo battery input through XT60 Connector
* Mini Rocker Switch
* Push Button
* LED (3mm)
* Electrolytic Capacitor (1000μF, 4700μF, 470μF)

## Mechanical Design
We've made our robot totally from scratch. Most of the parts of our robot are 3D printed, starting from chassis, wheels, and so on.

### Mechanical Parts List
* Axial Bearing (8mm x 16mm x 5mm)
* Axial Flange Bearing (3mm x 8mm x 4mm)
* M3 bolt
* M3 nut
* M2 bolt
* M2 nut
* M3 Hex Spacer

## Design Decisions
* We've designed a sonar mount which is mounted at the front and the side of the robot where the front-left and front-right sonar sensors are mounted at an angle of 52.5 degrees. Based on our testing, this is the optimal angle for the sonars to detect walls ahead of time, giving the bot enough time to react.
* We're using a Jetson Nano to handle the image processing algorithms. The Jetson Nano uses two cameras to detect towers and corner lines and sends the data to ESP32 via serial communication.
* The front axle is being articulated by the Servo Motor.
* To control our Motor we have used a TB6612FNG motor driver.
* MPU6050 was used to measure the real-time orientation of the robot and to help make the U-turn.
* A Buck-Boost modules were used for getting a constant output of 12V for the Motor
* Two buck module is used. One is for getting a constant 6V for the Servo, and the other one is for getting a constant 5V for the Jetson Nano as well as the ESP32.
* We used Ackerman steering as it is a vital steering geometry concept that enhances the handling and cornering performance of vehicles, making them safer and more efficient on the road. Ackerman steering, also known as Ackerman geometry or Ackerman principle, is a steering mechanism that is used in vehicles in order to enable proper turning of the wheels while maintaining optimal geometry and minimizing tire scrubbing during turns. It is commonly used in most modern vehicles, including cars, trucks, and other wheeled vehicles.
The fundamental idea behind Ackerman steering is that the inner and outer wheels of a vehicle must follow different turning radii during a turn, considering the varying angles of the front wheels. When a vehicle turns, the inner wheel needs to negotiate a tighter radius than the outer wheel to maintain a smooth turn without dragging or scuffing the tires. The Ackerman steering mechanism achieves this by using a steering linkage that connects the wheels. Typically, it consists of two tie rods connected to the steering arms on each wheel. The tie rods are connected to a central steering mechanism, such as a steering rack or a pitman arm, which is controlled by the driver. As the driver turns the steering wheel, the steering mechanism transfers the motion to the tie rods, causing the wheels to rotate accordingly. The geometry of the Ackerman steering mechanism ensures that the inner wheel turns at a sharper angle compared to the outer wheel, allowing both wheels to trace their respective turning radii accurately. By implementing Ackerman steering, vehicles can achieve better maneuverability, stability, and reduced tire wear during turns. It ensures that all wheels maintain proper contact with the road surface and minimizes the likelihood of skidding or slipping during turns.
![image](https://github.com/Ahnaf-nub/Mecha-404/assets/76505613/5aab9af5-65b7-4ce1-a794-1a9a6564b4d6)

* We also used a differential gearbox for the rear wheels. Although it uses a single DC motor, its primary purpose is to enable the wheels on a single axle to rotate at different speeds while receiving power from the engine and transmission. This crucial function allows for smooth and stable operation, particularly when the vehicle is turning. The differential works by distributing power from the input (usually the driveshaft) to the wheels through a system of gears, including a ring gear, side gears, and spider gears, all contained within a lubricated housing. It ensures that both wheels receive power, improving traction and stability, even in situations where one wheel loses traction. Different types of differentials are available to suit various vehicle needs and driving conditions, such as open differentials, limited-slip differentials, and locking differentials.
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/ccd4dbc3-0f39-403d-814e-50581b134f64)
