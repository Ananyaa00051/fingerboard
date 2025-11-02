

# 🖐️  Fingerboard

A real-time **gesture-controlled virtual whiteboard** built using **MediaPipe, OpenCV, and PyQt5**.
Draw, write, and select shapes **using just your hand — no mouse, no stylus, no touchscreen!**

---

## ✨ Features

| Feature                    | Description                               |
| -------------------------- | ----------------------------------------- |
| 👆 Finger-tracking         | Draw using your index finger in real-time |
| 🤖 MediaPipe Hand Tracking | Accurate landmark detection               |
| 🖌️ Freehand Drawing       | Smooth pencil-style sketching             |
| 📐 Shape Mode              | Draw lines, rectangles, and circles       |
| 🎨 Color Picker            | Choose brush colors                       |
| ✏️ Adjustable Brush Size   | Slider-based pen size control             |
| 💾 Save Canvas             | Export your drawing as an image           |
| 🧹 Clear Board             | Reset the whiteboard instantly            |
| ⚡ Real-time Performance    | 25–30+ FPS smooth rendering               |

---

## 🛠 Tech Stack

| Component       | Technology |
| --------------- | ---------- |
| Language        | Python     |
| Computer Vision | OpenCV     |
| Hand Tracking   | MediaPipe  |
| GUI Framework   | PyQt5      |
| Other           | NumPy      |

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/ai-finger-whiteboard.git
cd ai-finger-whiteboard
pip install opencv-python mediapipe pyqt5 numpy
```

---

## 🚀 Usage

### Run Script

```bash
python whiteboard_app.py
```

### Controls

| Action               | Key / Gesture                          |
| -------------------- | -------------------------------------- |
| Start / Stop Drawing | `D` key (freehand mode)                |
| Clear Canvas         | `C` key / Clear button                 |
| Save Drawing         | Save button                            |
| Pick Color           | Color button                           |
| Shape Mode           | UI buttons (Line / Rectangle / Circle) |
| Freehand Mode        | Freehand button                        |

---

## 📁 Project Structure

```
AI-Finger-Whiteboard/
│── whiteboard_app.py    # PyQt + MediaPipe app
│── README.md
│── whiteboard.png       # Sample saved output (generated)
└── requirements.txt
```

---

## 🧠 How It Works

* Captures video from webcam
* Uses **MediaPipe Hands** to detect hand + landmarks
* Tracks **index finger tip (landmark 8)**
* Draws trail on virtual canvas using OpenCV
* PyQt5 displays an interactive UI with tool controls

---

## 🚧 Future Improvements

* ✋ Multi-hand support
* ✨ Palm gesture shortcuts (erase, undo, color switch)
* 🧠 AI-based gesture recognition (thumbs-up, pinch, swipe)
* 💻 Support for smart boards & tablets

---

## 📜 License

MIT License

---

## 💡 Inspiration

Inspired by AR/VR human-computer interaction and markerless gesture-based design tools like Apple Vision Pro & Google's AI sandbox demos.

---

## ⭐ Show Support

If you like this project, please ⭐ the repo!

---

### 🎤 Author

**Annanya Sharma**
AI/ML Enthusiast

---

