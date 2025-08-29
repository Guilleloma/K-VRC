# K-VRC Raspberry Pi Project

[![K-VRC Demo](https://img.youtube.com/vi/sy0K2py56xU/0.jpg)](https://youtu.be/sy0K2py56xU)

## Table of Contents
1. [Overview](#overview)  
2. [Features](#features)  
3. [Hardware](#hardware)  
4. [3D Printing](#3d-printing)  
5. [Software Requirements](#software-requirements)  
6. [Installation & Setup](#installation--setup)  
7. [Usage](#usage)  
8. [Additional Notes](#additional-notes)  
9. [Development Process](#development-process)  
10. [License](#license)  
11. [Acknowledgments](#acknowledgments)

---

## Overview

This project is a **life-like replica** of **K-VRC**, a character from the Netflix series *Love, Death & Robots*. Our goal is to bring K-VRC to life through a combination of **3D printing**, **animatronics** (via a servo motor), a **camera**, an **OLED display**, and **audio capabilities**, all controlled by a **Raspberry Pi Zero 2W** running Python.

**Key highlights:**

- 3D-printed shell designed to replicate K-VRC's appearance.  
- **Servo** control for head or body movement.  
- **OLED SSD1360** display (I2C) for facial expressions or status indicators.  
- **Audio HAT WM8960** for audio output (and possibly input).  
- **OV564 camera** for vision-related features (e.g., face detection, object recognition, etc.).  
- Fully written in **Python** with libraries for hardware control, multimedia, and more.

You can visit the repository here:  
[**K-VRC GitHub Repository**](https://github.com/Guilleloma/K-VRC)

---

## Features

- **Servo SG90 control**: Provides simple, smooth animation for K-VRC's head or body movement.  
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
5. **Audio HAT WM8960** (check that it's designed for Raspberry Pi)  
6. **Camera module** (OV564 or equivalent that works with Pi Zero)  
7. **Wires, resistors**, and other electronics components (headers, connectors, etc.)  
8. **USB power supply** (5V, 2A minimum recommended)

**Optional / Recommended**:  
- **USB/HDMI adapters** or a Pi Zero interface kit for easier debugging.  
- **3D printer** (or 3D printing service) for creating the custom K-VRC shell.

---

## 3D Printing

1. **Model Files**  
   The 3D model files (STL or similar) for K-VRC's body will be located in the `3D_models` folder (or shared in the repository).  

2. **Recommended Settings**  
   - Material: PLA or ABS  
   - Layer Height: 0.2 mm  
   - Infill: Around 20% (depending on desired strength)  
   - Supports: May be required for certain overhangs depending on model orientation  

3. **Assembly**  
   - Print separate parts (head, body, legs) and assemble them using screws or adhesives as indicated.  
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
- `pyaudio` or custom libraries for WM8960 support (Ensure you configure the HAT's drivers on Raspberry Pi OS)

---

## Installation & Setup

1. **Clone the repository**:
   ```bash 
   git clone https://github.com/Guilleloma/K-VRC.git
   cd K-VRC
   ```

2. **Install Python dependencies**:
   ```bash
   pip3 install -r requirements.txt
   ```
   (Adjust the command if you use a virtual environment or a different Python version.)

3. **Activate the project's virtual environment**:
   ```bash
   source /home/pi/venvs/k-vrc-env/bin/activate
   ```
   
   This project uses a dedicated virtual environment located at `/home/pi/venvs/k-vrc-env/`. When the environment is activated, your terminal prompt will show `(k-vrc-env)` indicating that you're using the project's isolated Python environment.

4. **Enable I2C, Camera, and Audio on your Raspberry Pi**:
   ```bash
   sudo raspi-config
   ```
   Go to Interface Options and enable I2C and Camera.

   For the WM8960 Audio HAT, follow the vendor instructions (often involves installing kernel modules or editing /boot/config.txt).

Wire up the Hardware:

Connect the servo to a 5V pin, GND, and a GPIO pin on the Pi (e.g., GPIO18 for PWM).
Connect the OLED's SDA and SCL to the Pi's SDA/SCL I2C pins, and power lines to 3.3V/GND.
Attach the Audio HAT to the Pi Zero's GPIO header.
Ensure the camera connector is attached properly (CSI interface).
Test Each Component:
Servo: Run a simple PWM test script to move the servo.
OLED: Print "Hello World" to the display.
Audio: Play a sample WAV/MP3 and confirm audio output.
Camera: Use raspistill or similar commands to capture a test image.

## Usage

Run the main application using:
```bash
python main.py
```

The general workflow of the system is as follows:
- **Audio Capture:**  
  The `RealTimeAudioCapture` class (located in `chat/stt/audio_capture.py`) captures real-time audio and saves the recording to a temporary WAV file.
  
- **Voice Detection:**  
  The `is_audio_speech` function (in `chat/stt/stt_main.py`) computes the RMS of the recorded audio and compares it to the `SILENCE_THRESHOLD` (defined in `config.py`) to determine if speech is present.

- **Transcription and Conversation:**  
  If speech is detected, the audio file is sent to OpenAI Whisper via `transcribe_file` (in `chat/stt/stt_whisper_http.py`) to obtain a transcription. The transcription is then sent to OpenAI's Chat API (managed in `chat/chat_manager.py`) using the personality defined in `personality_system.txt` to set the character's persona.

- **Output and Animations:**  
  The chat response is printed to the console, and animations are triggered on the OLED display (controlled by `OledFaceController` in `face/oled_controller.py`). Additionally, if needed, servo movements can be executed via the controller in `movement/servo_controller.py`.

## Additional Notes

- To modify the robot's personality, edit the `personality_system.txt` file located at the project root.
- Adjust the audio capture parameters and other behaviors by modifying `config.py` as needed.
- Check out the example directories in `audio/audio_examples`, `servo_examples`, `face/oled_examples`, etc., for additional functionality and usage examples.
- Further details on internal workings (such as using the Whisper API or TTS control) can be found in the respective modules under `chat/stt`, `chat/tts`, and other directories.

## Development Process

This project follows a structured branching strategy to ensure code quality and stability:

- **trunk**: The main stable branch containing production-ready code.
- **development**: The integration branch where features are combined and tested.
- **feature branches**: Individual branches created from development for specific modifications.

### Workflow

1. All development work begins by creating a feature branch from the **development** branch.
2. Once a feature is complete, it's merged back into the **development** branch.
3. After thorough testing in the development branch, changes are merged into the **trunk** branch.

### Merge Guidelines

- We do not use fast-forward merges to maintain clear branch history.
- All merges require commit messages to document the purpose of the merge.
- This approach ensures that the repository history can be clearly visualized in tools like Gitgraph.

Contributors should follow this workflow to maintain project stability and facilitate collaborative development.

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
