# 🎯 AI Aim Assist

> Real-time AI-powered aim assistance using **YOLOv8** computer vision and **mouse movement automation**.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux-lightgrey)

---

## 📸 How It Works

1. **Screen capture** — grabs a configurable region of your screen at high speed
2. **Object detection** — runs YOLOv8 to find target classes (e.g. `person`, custom model)
3. **Target selection** — picks the closest target to the crosshair center
4. **Mouse movement** — smoothly moves the mouse toward the target using `win32api` or `pynput`
5. **Trigger logic** — optional auto-trigger when aim is close enough to target

```
┌─────────────────────────────────────────┐
│         Screen Region Capture           │
│                                         │
│   ┌────────────────────────────────┐    │
│   │  YOLOv8 Inference (GPU/CPU)   │    │
│   └────────────┬───────────────────┘    │
│                │  Detections            │
│   ┌────────────▼───────────────────┐    │
│   │    Target Picker (closest)    │    │
│   └────────────┬───────────────────┘    │
│                │  Target XY             │
│   ┌────────────▼───────────────────┐    │
│   │   Smooth Mouse Controller     │    │
│   └────────────────────────────────┘    │
└─────────────────────────────────────────┘
```

---

## ⚡ Features

- 🔍 **YOLOv8 detection** — swap any custom `.pt` model
- 🖱️ **Smooth aim** — configurable smoothing factor
- 🎮 **FOV control** — limit detection to a circular FOV zone
- 🔑 **Toggle hotkey** — press `F1` to toggle on/off
- 📦 **Headless or overlay mode** — optional real-time debug overlay window
- ⚙️ **config.yaml** — all settings in one file, no code edits needed
- 🖥️ **CUDA support** — automatically uses GPU if available

---

## 🛠️ Installation

### Requirements
- Python 3.10+
- Windows 10/11 (for `win32api`) or Linux
- NVIDIA GPU recommended (CUDA 11.8+) — CPU works but is slower

### 1. Clone the repo
```bash
git clone https://github.com/parx-rblox/ai-aim-assist.git
cd ai-aim-assist
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. (Optional) Install CUDA PyTorch for GPU acceleration
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

### 4. Configure
Edit `config.yaml` to set your target class, FOV, smoothing, and hotkey.

### 5. Run
```bash
python main.py
```

---

## ⚙️ Configuration (`config.yaml`)

```yaml
# Detection
model_path: "models/yolov8n.pt"   # path to your YOLO model
target_class: 0                    # 0 = person (COCO), -1 = all classes
confidence: 0.5                    # detection confidence threshold

# Screen capture region (centered on screen)
capture_width: 640
capture_height: 640

# Aim settings
fov_radius: 200                    # pixel radius to consider targets (0 = disabled)
smoothing: 6.0                     # higher = slower/smoother movement
aim_offset_x: 0                    # horizontal aim offset (e.g. for head offset)
aim_offset_y: -20                  # vertical aim offset (negative = aim higher)

# Trigger bot (auto-click when on target)
trigger_enabled: false
trigger_fov: 10                    # pixel radius for auto-trigger

# Controls
toggle_key: "F1"                   # hotkey to toggle aim assist on/off
overlay: true                      # show debug overlay window

# Hardware
device: "auto"                     # "auto", "cuda", or "cpu"
```

---

## 📁 Project Structure

```
ai-aim-assist/
├── main.py              # Entry point
├── config.yaml          # All user settings
├── requirements.txt     # Python dependencies
├── src/
│   ├── detector.py      # YOLOv8 inference wrapper
│   ├── capture.py       # Fast screen capture
│   ├── mouse.py         # Smooth mouse movement
│   ├── overlay.py       # Optional debug overlay
│   └── utils.py         # Helper functions
├── models/
│   └── .gitkeep         # Place your .pt model files here
└── README.md
```

---

## 🤝 Contributing

Pull requests are welcome! Open an issue first for major changes.

---

## ⚠️ Disclaimer

This project is for **educational purposes only** — computer vision, input automation, and real-time AI inference.
Using aim assist software in online games violates most games' Terms of Service and can result in bans.
The author is not responsible for any misuse.

---

## 📄 License

MIT © parx-rblox
