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


