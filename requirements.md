# Project Requirements: MoodDJ-v2

## 1. Project Overview
**Project Name:** MoodDJ-v2  
**Team Name:** the sinners  
**Team Leader:** Srivathsan R  
**Description:** An AI-powered, hands-free music companion that transforms music listening from a passive activity into an active, context-aware experience. The system creates hyper-personalized soundtracks by analyzing facial expressions, voice commands, weather conditions, and time of day in real-time.

---

## 2. Problem Statement
* **Passive Interaction:** Traditional streaming services (Spotify, Apple Music) require manual input, leading to a disconnect between the user's current state and the music played.
* **Decision Fatigue:** Users spend time and energy searching for the "perfect song," disrupting their flow state.
* **Context Blindness:** Standard apps rely on generic static playlists (e.g., "Sad Hits") that fail to account for environmental nuances (e.g., rain vs. sun).

---

## 3. Functional Requirements

### 3.1 Input Processing
* **Visual Input:** The system must capture video feed via webcam to detect user facial expressions.
* **Audio Input:** The system must support voice commands (e.g., "Play energetic songs") in multiple languages (English, Hindi, Tamil, Telugu).
* **Environmental Input:** The system must retrieve geolocation data to fetch real-time weather conditions and time of day.

### 3.2 Core Logic & AI
* **Emotion Detection:** The system must use a Residual Masking Network (RMN) to classify emotions from video frames.
* **Mood Locking:** The system must aggregate 5 consecutive frames to establish "mood stability" to prevent jarring music changes due to blinking or looking away.
* **Context Synthesis:** The system must combine Emotion, Weather, and Time into a comprehensive prompt.
* **Playlist Curation:** The system must use an LLM (via Groq API) to generate a song list based on the synthesized context.

### 3.3 Audio Playback
* **Stream Generation:** The system must utilize `yt-dlp` to search and stream high-quality audio.
* **Quality Filtering:** The system must automatically filter out low-quality content (Shorts, 1-hour loops) to prioritize official audio.
* **Latency:** Audio playback should initiate with minimal delay after mood detection.

### 3.4 User Interface
* **Dynamic Theming:** The UI color scheme must automatically shift to reflect the detected mood (e.g., Blue for Calm, Red for Energetic).
* **Real-time Feedback:** The UI must display the currently detected emotion and weather status.

---

## 4. Non-Functional Requirements
* **Performance:** LLM inference must occur in sub-second timeframes using LPU hardware (Groq).
* **Scalability:** The backend must handle asynchronous requests via WebSockets to support real-time data flow.
* **Privacy:** Video feed data should be processed for emotion detection and not permanently stored without user consent.
* **Usability:** The application must be "hands-free," requiring no physical interaction once started.

---

## 5. Technology Stack Requirements
* **Frontend:** React, Vite, TailwindCSS
* **Backend:** Python, FastAPI
* **Communication:** WebSockets
* **AI/ML:** RMN (Vision), Llama-3 (LLM on Groq)
* **External APIs:** Open-Meteo (Weather), yt-dlp (Audio source)

---

## 6. Future Scope (Roadmap)
* **User Accounts:** MongoDB integration for mood history and analytics.
* **Platform Integration:** OAuth support for Spotify/Apple Music library syncing.
* **Wearables:** Integration with Fitbit/Apple Watch for biometric stress detection.
* **Mobile:** React Native app development.
