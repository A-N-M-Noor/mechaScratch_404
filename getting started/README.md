# Getting Started
We are using a **NVIDIA Jetson Nano Developer Kit** for object detection, and an **ESP32 Microcontroller** for the sensors and for handling the controls. So before anything, you must set up your Jetson Nano and ESP32.

## Setting up the Jetson Nano
Detailed instructions can be found on [NVIDIA's official website](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/b30dbf15-980d-4c74-9ec6-5685efd21a3e)

The **NVIDIA Jetson Nano Developer Kit** is a small single-board computer. You'll need to flash an operating system (usually Ubuntu) in a micro SD card and insert it into the Jetson Nano. So, you'll need - 
* A micro SD card (32GB or 64GB)
* Micro-USB supply/adapter (Should be at least 10W)
* USB keyboard and mouse
* Computer display with HDMI cable (You can use a VGA Cable too, but you'll need an HDMI to VGA Converter)

### Flashing an SD card
To prepare your microSD card, you’ll need a computer with an Internet connection and the ability to read and write SD cards via a built-in SD card slot or adapter.
1. Download the [Jetson Nano Developer Kit SD Card Image](https://developer.nvidia.com/jetson-nano-sd-card-image)
2. Format your SD card
3. Install an image writer application. We've used [Etcher](https://etcher.balena.io/)
4. Click **Select Image** and select the image file you've downloaded just now.

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/cd6eaa0c-ff47-47a7-8f52-b617cc47f696)

5. Insert your SD card and select the SD drive from **Select Drive**, then click **Flash!**

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/fdcd5679-c184-4fd2-b6e7-a8bf1165cea2)

6. After it's done flashing the image, you can eject your SD card from your device.

### Setup and First Boot
Insert the SD card in the SD slot of your jetpack and power it up. For the first boot, you'll need to use a monitor, keyboard and mouse. Also, connect a wifi dongle to the jetpack if you don't have the network card installed with it.

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/1e8d64e3-7c4d-430f-a153-4e9937bc37bf)

A green LED next to the Micro-USB connector will light as soon as the developer kit powers on. When you boot the first time, the developer kit will take you through some initial setup, including:
* Review and accept NVIDIA Jetson software EULA
* Select system language, keyboard layout, and time zone
* Create username, password, and computer name
* Select APP partition size—it is recommended to use the max size suggested

Now you'll be able to use the Jetson Nano as you would use any other Ubuntu PC. But we want to use it without any monitor or keyboard and mouse attached. So we'll use a Remote desktop application (VNC for example).

### Setting up VNC
Now, Jetson comes with "Desktop Sharing" installed. But it fails due to a bug. To solve this issue -
1. Install "nano", which is a command used to edit files from the terminal. To install "nano", open up a terminal and write
```
sudo apt install nano
```
2. First, we will edit the _org.gnome.Vino_ schema, as it has a missing parameter called enabled. Open the schema:
```
sudo nano /usr/share/glib-2.0/schemas/org.gnome.Vino.gschema.xml
```
3. Add the missing key (any location will do):
```XML
<key name='enabled' type='b'>
   <summary>Enable remote access to the desktop</summary>
   <description>
   If true, allows remote access to the desktop via the RFB
   protocol. Users on remote machines may then connect to the
   desktop using a VNC viewer.
   </description>
   <default>false</default>
</key>
```
4. Compile the new Gnome schema configuration:
```
sudo glib-compile-schemas /usr/share/glib-2.0/schemas
```
5. Update the Desktop Sharing settings. Your application should work now. Launch it from your Jetson Nano desktop and change the settings as it suits you.
6. Setup the VNC server to autostart
   - Open the Startup Application Preferences panel
   - Add your VNC (Vino) entry: Add a name ('Vino'), a description (any text which makes sense to you) and the command: ```/usr/lib/vino/vino-server```. Close the app.
7. Disable encryption for the VNC server
   ```
   gsettings set org.gnome.Vino require-encryption false
   gsettings set org.gnome.Vino prompt-enabled false
   ```
8. Reboot

After reboot, you can use any [VNCViewer](https://www.realvnc.com/en/connect/download/viewer/) from your laptop to connect to the shared screen.

### Python and Python Modules
Jetson comes with Python 2.7 and Python 3. For this project, we'll use Python3. But we'll need to install a few libraries.
* OpenCV
* Numpy
* pySerial

First, update and upgrade your package manager:
```
sudo apt-get update
sudo apt-get upgrade
```

Install 'pip' aka python package manager, and build-essentials:
```
sudo apt install -y python3-pip
sudo apt install build-essential libssl-dev libffi-dev python3-dev
```

Now install OpenCV:
```
sudo apt install python3-opencv
```
Install numpy:
```
pip3 install numpy
```
Install pyserial:
```
pip3 install pyserial
```

## Setting up the ESP32

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/b2427834-0830-4407-ba09-913bf4438765)

ESP32 is a pretty powerful microcontroller. It is a dual-core 32-bit MCU, which means we can run two loops in parallel which would make our robot a lot faster. To keep it simple, we'll use the Arduino IDE to compile codes for the ESP32 Microcontroller.

### Installation
* Download and install the [Arduino IDE](https://www.arduino.cc/en/software). As of now, the latest version is `2.2.1`, but it lags on a low-end device. So install the Legacy IDE (`1.8x`) for now.

![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/51009def-76e4-4f8b-b5f6-feb5da4c1bc0)

* In your Arduino IDE, go to File > Preferences, and enter the following into the "Additional Board Manager URLs" field, and click OK: 
```
https://raw.githubusercontent.com/espressif/arduino-esp32/gh-pages/package_esp32_index.json
```
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/1deebbbf-92e0-4f38-a313-d06a5578e660)

* Open the Arduino Boards Manager: `Tools > Board > Boards Manager...` and search for **ESP32**. Find the one named "ESP32 by Espressif Systems" and click on "Install".
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/d2d5850e-1a15-4024-96b8-57f9c464a54a)

* Install the necessary libraries:
   - Go to `Sketch > Include Libraries > Manage Libraries...`
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/7d42419a-1a90-4b84-be27-7d867faaaf8e)
   - Find and install **"ESP32Servo"** by _"Kevin Harrington"_ and **"NewPing"** by _"Tim Eckel"_.
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/94853da6-6f67-49e4-bb73-82e491525fd6)
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/8579493f-ba9f-4091-ab5d-c0f22b2c44a4)


* Select your Board in the `Tools > Board` menu. Select the one named "ESP32 Dev Module". This one works for almost every ESP32 board.
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/40ef4c0d-407d-467f-91c7-f47dd302f126)

* When you need to upload a code, select the port from `Tools > Port` and hit upload.
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/3fb264b6-173a-4ae2-a552-cd9be82e8ba9)
![image](https://github.com/A-N-M-Noor/mechaScratch_404/assets/113457396/f50c42d9-64d7-4af0-9547-e3d8492c68a5)

Now, depending on what ESP32 board you're using, you might not be able to upload the code just yet (There are some knock-off versions available in the market). Install the [CP2102 Driver](https://www.silabs.com/documents/public/software/CP210x_Windows_Drivers.zip) and try again. It should work now.
_______

Source:
* [https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit](https://developer.nvidia.com/embedded/learn/get-started-jetson-nano-devkit)
* [https://raspberry-valley.azurewebsites.net/NVIDIA-Jetson-Nano/](https://raspberry-valley.azurewebsites.net/NVIDIA-Jetson-Nano/)
