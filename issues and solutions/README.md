# Issues we've faced and how we worked around it

## Color Detection
Detecting colors using RGB color space gives unreliable outcomes. The reason is, that a bright red color and a dark red color have completely different values in RGB color space. But if HSV color space is used instead, these color values become much more reliable.

The HSV color code, also known as HSB (Hue, Saturation, Brightness), is a color model used to describe and represent colors in terms of three fundamental attributes: hue, saturation, and brightness. It is often used in computer graphics, image processing, and design applications. Here's a brief explanation of each component:

* **Hue (H):** Hue refers to the dominant color in a particular shade. It is measured in degrees on a color wheel, typically ranging from 0 to 360 degrees. In this representation, 0° corresponds to red, 120° to green, and 240° to blue, with the other colors filling the spectrum in between.

  _However, in OpenCV, the range for hue is from 0 to 180._

* **Saturation (S):** Saturation indicates the intensity or purity of the color. It is usually represented as a percentage and ranges from 0% (completely unsaturated, grayscale) to 100% (fully saturated, vibrant color). Higher values result in more vivid colors, while lower values approach grayscale.

  _However, in OpenCV, the range for saturation is from 0 to 255._

* **Brightness (V or B):** Brightness represents the lightness or darkness of a color. It is also typically expressed as a percentage, with 0% being completely black and 100% being the full brightness of the color at its specified hue and saturation.

  _However, in OpenCV, the range for brightness is from 0 to 255._
  
  
<img align="middle" alt="HSV" width="350" src="https://github.com/tajwarTX/test/assets/113457396/08ebdea5-9612-493a-9cee-11e7c33df9f2">
  
  
By combining these three components (H, S, and V), you can specify a wide range of colors. And HSV color space somewhat represents the way humans perceive colors. This makes the HSV color model a more intuitive and user-friendly way to describe and select colors compared to other color models like RGB or CMYK, which are based on the additive or subtractive properties of light.

## Serial communication
The jetson nano and esp32 use serial communication to exchange data. But the sent and received data was turning into garbage values on both the jetson and esp32 side. To overcome the issue of data corruption during serial communication between the Jetson Nano and ESP32, a revised approach was adopted. Instead of sending all the data in a single block, it was segmented into key-value pairs. In this setup, the key ranges from 0 to 49, and the value ranges from 50 to 250. Since both key and value fall within the 0-255 range, they can be transmitted as 8-bit codes.

The communication process unfolds as follows:

1. The ESP32 initiates the data request from the Jetson.
2. The Jetson, in response, sends the data in a specific sequence, starting with a key and followed by a corresponding value.
3. Upon receiving a key, the ESP32 anticipates the next value to follow. For instance, if the ESP32 receives the key '6,' it interprets this as an identifier for the upcoming value.
4. However, to determine the accurate value, the ESP32 subtracts 50 from the received value, as the values commence from 50.

This data exchange approach ensures reliable communication between the Jetson Nano and ESP32, allowing for the accurate transmission and interpretation of information without the risk of data corruption.

Here's the list of key-value pairs we've used in our program:
* 5 - Object type
* 6 - Object position (x position)
* 7 - Object distance
* 8 - Turn count
* 10 - Track direction

## The robot randomly bumps into objects

<img align="right" width="420" src="https://github.com/tajwarTX/test/assets/136412241/f802a384-653b-4f41-8f8f-881cbcc15142">

The robot encounters occasional instances where it unintentionally collides with walls or some towers. To mitigate this issue, a collision avoidance algorithm has been implemented. When the robot detects objects in close proximity, it responds by executing a brief backward movement, effectively reversing its direction for a short distance. Following this reverse action, the robot proceeds with its regular course of operation, thereby minimizing the impact of accidental collisions and promoting smoother navigation.





## Issues with the back camera
In the initial plan, a dedicated camera (Raspberry pi camera v2.1) was positioned at the back of the robot, facing downward, with the sole purpose of counting the corner lines. However, there was an issue with the feed from the Pi-camera, which exhibited a persistent purple hue. To address this problem, adjustments were made, involving white balancing and color correction to rectify the color distortion.

As the robot's speed increased, particularly during the open round, the downward-facing Pi-camera struggled to keep pace and occasionally missed detecting some of the lines. In response to these challenges, a decision was made to streamline the setup by utilizing a single camera for both tower and line detection, simplifying the hardware configuration and enhancing overall efficiency.

## After passing an object, the robot misses the next one
When the robot encounters a tower, particularly in the corners, it may intermittently lose sight of the next tower, causing it to deviate from its intended path. This deviation can result in the robot's movement resembling the following pattern:
  
  
<img align="middle" alt="Miss" width="500" src="https://github.com/tajwarTX/test/assets/113457396/d9184386-c198-4cd3-a158-f67a2dc9560a">
  
To address the challenge of losing sight of the next tower after passing one, the robot has implemented two key strategies:

1. **Momentary Steering Correction:** Immediately after passing an object, the robot briefly steers in the opposite direction, counteracting the previous turn. If the last detected object was red, it steers to the left, and if it was green, it steers to the right, straightening its direction a bit. This corrective action helps the robot align itself and regain its intended path.

2. **Corner Detection and Adaptive Turning:** As soon as the robot identifies a corner in the track, it executes a brief turn towards the direction of the track. However, it promptly ceases this turning action upon detecting an object. This approach allows the robot to effectively navigate corners while remaining responsive to obstacles.

This way, the robot manages to handle the corners better.

  
<img align="middle" alt="Find" width="500" src="https://github.com/tajwarTX/test/assets/113457396/2c0afb30-7f03-4406-b705-969cc0489e8f">


These two strategies work in tandem to enhance the robot's ability to maintain a consistent and accurate course, especially when negotiating corners and navigating between towers.
