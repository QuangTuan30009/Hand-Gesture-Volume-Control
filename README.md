# Hand-Gesture-Volume-Control

Control system volume on Windows using hand gestures via webcam. Tracks thumb and index finger distance to adjust volume.

## Features
- Real-time hand tracking with MediaPipe.
- Adjusts volume based on thumb-index finger distance.
- Displays hand landmarks, distance, and volume percentage.

## Requirements
- Python 3.6+
- `opencv-python`, `mediapipe`, `pycaw`, `comtypes`

## Installation
1. Clone the repo:
   ```bash
   git clone https://github.com/QuangTuan30009/hand-gesture-volume-control.git

## Notes
Windows only (uses pycaw).
Adjust sensitivity in code if needed (distance * 200).
## License
MIT License
