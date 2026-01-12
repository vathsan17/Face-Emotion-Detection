# 🎧 MoodDJ: AI-Powered Emotion & Music Ecosystem

**MoodDJ** is a sophisticated computer vision ecosystem that bridges the gap between human emotions and music. By leveraging state-of-the-art Deep Learning (Residual Masking Networks), it analyzes your real-time facial expressions to curate a personalized Spotify listening experience.

---

## ⚡ Core Applications

The project is divided into three distinct modules to cater to different user needs:

### 1. 🔍 MoodDJ Live (Primary App)
*File: `frontend/frontend_simple.py`*
* **Real-time Scanning:** Uses your webcam to detect and lock onto your dominant emotion using a frame-buffer for stability.
* **Spotify Integration:** Automatically embeds a Spotify player for the detected mood.
* **Interactive Hotkeys:**
    * **[Space Hold]:** Trigger a re-scan.
    * **[Double Space]:** Skip to the next track.
    * **[Triple Space]:** Go back to the previous track.
    * **[L]:** "Like" a song (saves it to your favorites in MongoDB).
* **Voice Feedback:** Integrated Text-to-Speech (TTS) for hands-free interaction.

### 2. 📊 Insights Dashboard
*File: `frontend/dashboard.py`*
* **Analytics:** Visualize your mood trends and listening history over time.
* **KPIs:** Track your dominant mood, total sessions, and favorite songs.
* **Interactive Charts:** Powered by **Plotly** for beautiful, dark-themed data visualization.

### 3. 🧪 Simple MoodMatcher (Legacy)
*File: `frontend/app.py`*
* A lightweight, snapshot-based version using `DeepFace` for quick mood checks without real-time streaming.

---

## 🛠️ Technology Stack

| Component | Technology | Role |
| :--- | :--- | :--- |
| **Frontend** | [Streamlit](https://streamlit.io/) | Web UI & Application logic. |
| **CV Engine** | [OpenCV](https://opencv.org/) | Camera handling & image processing. |
| **AI Model** | [RMN](https://github.com/matsui528/rmn) | Residual Masking Network for high-accuracy emotion detection. |
| **Database** | [MongoDB](https://www.mongodb.com/) | Stores song library, user history, and likes. |
| **Visuals** | [Plotly](https://plotly.com/) | Real-time data visualization and charts. |
| **Audio** | [Spotify API](https://developer.spotify.com/) | Official embeds for seamless playback. |
| **Voice** | [Pyttsx3](https://pypi.org/project/pyttsx3/) | Offline text-to-speech for interactivity. |

---

## 📂 Project Structure

```plaintext
Face-Emotion-Detection-vazanly/
├── frontend/
│   ├── frontend_simple.py    # Main AI Music Player
│   ├── dashboard.py          # Analytics & History Dashboard
│   └── app.py                # Snapshot-based Legacy Version
│
├── backend/
│   ├── models/               # AI Model weights & configs
│   ├── db_setup.py           # Database seeding script (Run first!)
│   ├── check_stats.py        # CLI for DB verification
│   └── simple_emotion.py     # CLI-based pure emotion scanner
│
├── .gitignore                # Environment & model exclusions
└── README.md                 # This file
```

---

## ⚙️ Setup & Installation

### 1. Prerequisites
* **Python 3.8+**: (3.11 recommended for stability with MediaPipe/RMN).
* **MongoDB Community Server**: Must be installed and running on `localhost:27017`.
* **GitHub Limits**: Note that large binary files are excluded via `.gitignore` and must be downloaded manually.

### 2. Clone and Install dependencies
```bash
git clone https://github.com/your-username/Face-Emotion-Detection-vazanly.git
cd Face-Emotion-Detection-vazanly
pip install -r requirements.txt
```

### 3. ⚠️ Manual Model & Asset Setup (REQUIRED)
Due to GitHub tracking limits, the following large files are **not included** in the repository. You must ensure they are in the correct directories:

| Asset | Path | Purpose |
| :--- | :--- | :--- |
| **RMN Weights** | `backend/models/pretrained_ckpt/` | Core weights for the Residual Masking Network. |
| **SSD Model** | `backend/models/res10_300x300_ssd_iter_140000.caffemodel` | Caffe-based face detector. |
| **SSD Config** | `backend/models/deploy.prototxt.txt` | Configuration for the face detector. |

### 4. Database Initialization
Populate your local MongoDB with the song library before starting:
```bash
python backend/db_setup.py
```

---

## 🚀 How to Run

### Run the Main Player:
```bash
streamlit run frontend/frontend_simple.py
```

### View Your Analytics:
```bash
streamlit run frontend/dashboard.py
```

---

## 📸 Screenshots

*(Add your screenshots here to make the README pop!)*

| Mood Player | Analytics Dashboard |
| :---: | :---: |
| ![Mood Player Placeholder](https://via.placeholder.com/400x250.png?text=MoodDJ+Player+Interface) | ![Dashboard Placeholder](https://via.placeholder.com/400x250.png?text=Analytics+Dashboard) |

---

## 🔧 Troubleshooting

* **Camera issues:** Ensure no other applications (Zoom, Teams, etc.) are using your webcam.
* **Database Connection:** Make sure MongoDB service is running. You can check this by running `services.msc` on Windows and looking for "MongoDB Server".
* **Keyboard Hotkeys:** The `keyboard` library may require administrator privileges on some systems to capture global hotkeys.
* **Audio/Speech:** If you don't hear any voice feedback, ensure your system's default TTS engine is configured correctly.

---

## 🌟 Key Features Walkthrough

1.  **Stability First**: Unlike simple detectors that flip-flop between emotions, MoodDJ uses an **emotion buffer**. It waits for 15 consistent frames before "locking" your mood to ensure the music matches how you *actually* feel.
2.  **Product Feel**: The UI is designed with a premium, Spotify-inspired dark aesthetic, utilizing custom CSS and responsive layouts.
3.  **Hardware Interaction**: Use the spacebar on your keyboard to control the interface without looking away from the camera.
4.  **Local Intelligence**: All AI processing happens locally on your machine for privacy and speed.

---

## 🤝 Contributing
Contributions are welcome! Whether it's adding more songs to `db_setup.py`, improving the AI model, or enhancing the Streamlit UI, feel free to fork and submit a PR.

---

## 📜 License
Developed for the Face-Emotion Detection Hackathon.
