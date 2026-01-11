# 🎵 SpotifyFaceAI - Emotion-Based Music Recommendation & Analysis

**SpotifyFaceAI** is an intelligent computer vision application that detects facial emotions in real-time and provides interactive feedback, such as recommending music based on your mood. 

Built with **Streamlit**, **OpenCV**, and state-of-the-art Deep Learning models (**DeepFace** & **RMN**).

---

## 📂 Project Architecture

The project is organized into a clean **Frontend vs Backend** structure to separate the user interface from core logic and models.

```plaintext
SpotifyFaceAI/
├── frontend/                 # Streamlit Web Applications
│   ├── app.py                # Main Application: MoodMatcher (DeepFace + Mock Spotify)
│   └── frontend_simple.py    # Dashboard: Real-time Emotion Scanner (RMN)
│
├── backend/                  # Core Logic & Scripts
│   ├── simple_emotion.py     # CLI/Window-based Detector (OpenCV + RMN)
│   └── models/               # AI Models & Weights
│       ├── deploy.prototxt.txt
│       ├── res10_300x300_ssd_iter_140000.caffemodel
│       └── pretrained_ckpt/  # (Ignored in Git, manually placed)
│
├── .gitignore                # Git Configuration (Excludes large models)
└── README.md                 # Project Documentation
```

---

## ✨ Features

### 1. MoodMatcher (`frontend/app.py`)
A music recommendation engine driven by your face.
- **How it works:** Captures a snapshot, analyzes it using `DeepFace`, and queries a Mock Spotify Database for a song matching the emotion.
- **Emotions Supported:** Happy, Sad, Angry, Neutral, Surprise.
- **Tech**: `Streamlit`, `DeepFace`, `NumPy`.

### 2. AI Emotion Scanner (`frontend/frontend_simple.py`)
A real-time analytical dashboard.
- **How it works:** Streams video from your webcam, detects faces using `RMN`, and overlays a high-confidence emotion label with a visual confidence bar.
- **Tech**: `Streamlit`, `RMN`, `OpenCV` (Video Processing).

### 3. Simple Detector CLI (`backend/simple_emotion.py`)
A lightweight, window-based application.
- **How it works:** Opens a raw OpenCV window with bounding boxes and emotion labels. Ideal for testing model performance without a web UI.
- **Tech**: `OpenCV`, `RMN`.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Frontend Framework** | [Streamlit](https://streamlit.io/) | Interactive web UI for Python scripts. |
| **Computer Vision** | [OpenCV](https://opencv.org/) | Image processing and webcam stream handling. |
| **Deep Learning (1)** | [DeepFace](https://github.com/serengil/deepface) | Used in `app.py` for mostly likely emotion analysis. |
| **Deep Learning (2)** | [RMN](https://github.com/matsui528/rmn) | Residual Masking Network. Highly accurate real-time detection. |
| **Face Detection** | SSD & ResNet | Caffe-based Single Shot Detector for finding faces rapidly. |

---

## ⚙️ Setup & Installation

### 1. Prerequisites
- Python 3.8 or higher
- A working webcam

### 2. Clone the Repository
```bash
git clone https://github.com/your-username/SpotifyFaceAI.git
cd SpotifyFaceAI
```

### 3. Install Dependencies
```bash
pip install streamlit opencv-python numpy deepface rmn pillow
```

### 4. ⚠️ Manual Model Setup (CRITICAL)
Due to file size limits, the `pretrained_ckpt` folder (approx 500MB) for the RMN model is **excluded from Git**.

**If you are cloning this for the first time on a new machine:**
1. Download or copy the `pretrained_ckpt` folder.
2. Place it exactly at: `backend/models/pretrained_ckpt/`.

---

## 🚀 Usage Guide

### Running MoodMatcher
Best for: Getting a music recommendation.
```bash
streamlit run frontend/app.py
```

### Running Emotion Scanner
Best for: Real-time analysis and dashboarding.
```bash
streamlit run frontend/frontend_simple.py
```

### Running Simple Detector
Best for: Quick debugging or lightweight usage.
```bash
python backend/simple_emotion.py
```
*(Press `q` to quit the window)*

---

## 🔧 Troubleshooting

- **Camera not opening?**
  - Ensure no other app (Zoom, Teams) is using the camera.
  - Restart your terminal or computer if the camera is "busy".
- **AttributeError / Import Errors?**
  - Verify you are in the root `SpotifyFaceAI` folder when running commands.
  - Check that virtual environment is activated if you used one.
- **Model not found?**
  - Double-check the **Manual Model Setup** step. The code looks for models in specific paths.

---

*Developed for the SpotifyFaceAI Project.*
