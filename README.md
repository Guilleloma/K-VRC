# K-VRC Raspberry Pi Project

![Cheeky_kvrc](https://github.com/user-attachments/assets/78056914-b316-40cc-9b1a-54c4a7994b1d)

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Hardware](#hardware)  
4. [3D Printing](#3d-printing)  
5. [Software Requirements](#software-requirements)  
6. [Installation & Setup](#installation--setup)  
7. [Usage](#usage)   
8. [License](#license)  
9. [Acknowledgments](#acknowledgments)

---

## Overview

This project is a **life-like replica** of **K-VRC**, a character from the Netflix series *Love, Death & Robots*. Our goal is to bring K-VRC to life through a combination of **3D printing**, **animatronics** (via a servo motor), a **camera**, an **OLED display**, and **audio capabilities**, all controlled by a **Raspberry Pi Zero 2W** running Python.

**Key highlights:**

- 3D-printed shell designed to replicate K-VRC’s appearance.  
- **Servo** control for head or body movement.  
- **OLED SSD1360** display (I2C) for facial expressions or status indicators.  
- **Audio HAT WM8960** for audio output (and possibly input).  
- **OV564 camera** for vision-related features (e.g., face detection, object recognition, etc.).  
- Fully written in **Python** with libraries for hardware control, multimedia, and more.

You can visit the repository here:  
[**K-VRC GitHub Repository**](https://github.com/Guilleloma/K-VRC)

---

## Features

- **Servo SG90 control**: Provides simple, smooth animation for K-VRC’s head or body movement.  
- **OLED I2C (SSD1360)** support: Displays text, images, or animations that add expressive features.  
- **Audio playback and recording** via the WM8960 Audio HAT.  
- **Camera integration (OV564)**: Potential for image capture, video streaming, or computer vision tasks.  
- **Python-based**: Easy to customize, extend, and maintain. Works with the standard Python ecosystem.

---

## Hardware

To replicate or build this project, you will need the following hardware:

1. **Raspberry Pi Zero 2W** (Core computing unit)  
2. **MicroSD card** (16GB or more recommended)  
3. **Servo motor** (SG90 or compatible 5V servo)  
4. **OLED SSD1360** display (I2C interface)  
5. **Audio HAT WM8960** (check that it’s designed for Raspberry Pi)  
6. **Camera module** (OV564 or equivalent that works with Pi Zero)  
7. **Wires, resistors**, and other electronics components (headers, connectors, etc.)  
8. **USB power supply** (5V, 2A minimum recommended)

**Optional / Recommended**:  
- **USB/HDMI adapters** or a Pi Zero interface kit for easier debugging.  
- **3D printer** (or 3D printing service) for creating the custom K-VRC shell.

---

## 3D Printing

1. **Model Files**  
   The 3D model files (STL or similar) for K-VRC’s body will be located in the `3D_models` folder (or shared in the repository).  

2. **Recommended Settings**  
   - Material: PLA or ABS  
   - Layer Height: 0.2 mm  
   - Infill: Around 20% (depending on desired strength)  
   - Supports: May be required for certain overhangs depending on model orientation  

3. **Assembly**  
   - Print separate parts (head, body, arms, etc.) and assemble them using screws or adhesives as indicated.  
   - Ensure you leave space for the servo, OLED, and other electronics before final assembly.

---

## Software Requirements

- **Operating System**: Raspberry Pi OS (Bullseye or later recommended)  
- **Python 3** (3.7+ recommended)  
- **Git** (for cloning this repository)  

### Python Libraries

Below is a non-exhaustive list of Python libraries commonly used in this project (see `requirements.txt` in the repository for the latest list):

- `RPi.GPIO` or [`gpiozero`](https://gpiozero.readthedocs.io/en/stable/) for GPIO pin control  
- `smbus` or `Adafruit_SSD1306`/`Adafruit_CircuitPython_SSD1306` (depending on how you manage the OLED)  
- `pyttsx3` or other TTS libraries if you wish to add text-to-speech  
- `opencv-python` (OpenCV) if camera-based image processing is required  
- `numpy` for any advanced image/audio or data manipulation  
- `pyaudio` or custom libraries for WM8960 support (Ensure you configure the HAT’s drivers on Raspberry Pi OS)

---

## Installation & Setup

1. **Clone the repository**:
   ```bash 
   git clone https://github.com/Guilleloma/K-VRC.git
   cd K-VRC
2. **Install Python dependencies**:
```bash
   pip3 install -r requirements.txt
```
(Adjust the command if you use a virtual environment or a different Python version.)

3.**Enable I2C, Camera, and Audio on your Raspberry Pi**:
```bash
Run sudo raspi-config
```
Go to Interface Options and enable I2C and Camera.

For the WM8960 Audio HAT, follow the vendor instructions (often involves installing kernel modules or editing /boot/config.txt).
Wire up the Hardware:

Connect the servo to a 5V pin, GND, and a GPIO pin on the Pi (e.g., GPIO18 for PWM).
Connect the OLED’s SDA and SCL to the Pi’s SDA/SCL I2C pins, and power lines to 3.3V/GND.
Attach the Audio HAT to the Pi Zero’s GPIO header.
Ensure the camera connector is attached properly (CSI interface).
Test Each Component:
Servo: Run a simple PWM test script to move the servo.
OLED: Print “Hello World” to the display.
Audio: Play a sample WAV/MP3 and confirm audio output.
Camera: Use raspistill or similar commands to capture a test image.

## Usage
Once everything is set up, power on the Raspberry Pi Zero 2W and navigate to the project directory. You can run the main Python script (for example, main.py) using:

```bash
python3 main.py
```
Depending on how you structure your code, this script might do any of the following:

Initialize servo movement (like K-VRC “waking up”).
Display an animated or static image on the OLED screen.
Start audio feedback or voice-based interactions.
Initialize camera functions (e.g., object detection, streaming, etc.).
Check the console or the OLED for status messages. Detailed logs may be stored in a dedicated logs/ folder or printed to the terminal.

## License
This project is distributed under the MIT License. For more details, see the LICENSE file in the repository.

## Acknowledgments
Inspired by the character K-VRC from Love, Death & Robots
Special thanks to the open-source community for Python libraries and Raspberry Pi resources
Raspberry Pi Foundation for providing the hardware and extensive documentation
For any questions, suggestions, or troubleshooting, feel free to open an Issue on this repository or contact the maintainers.

Enjoy bringing K-VRC to life!
Feel free to reach out via the GitHub Issues page if you encounter any challenges or want to share updates on your build.

Happy building and hacking!🤖
