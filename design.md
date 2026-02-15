# System Design Document: MoodDJ-v2

## 1. High-Level Architecture
The system follows a Client-Server architecture heavily relying on Asynchronous communication (WebSockets) to ensure real-time responsiveness.

### 

[Image of client server architecture diagram with websockets]


* **Client (Frontend):** Captures sensory data and renders the dynamic UI.
* **Server (Backend):** Orchestrates AI models, fetches external data, and streams audio.
* **AI Engine:** Dedicated modules for Computer Vision (RMN) and Text Generation (Groq).

---

## 2. Component Design

### 2.1 Frontend (React + Vite)
* **Video Capture Module:** Uses HTML5 `getUserMedia` to grab webcam frames.
* **Canvas Processor:** Slices frames and sends them to the backend via WebSocket.
* **Dynamic Theme Engine:** Uses TailwindCSS variables to update the DOM's primary colors based on the `mood_state` received from the backend.
* **Audio Player:** HTML5 Audio element receiving stream URLs.

### 2.2 Backend (FastAPI + Python)
* **WebSocket Manager:** Handles persistent connections, receiving frames and sending audio chunks.
* **Orchestrator:**
    1.  Receives Frame -> Sends to **RMN Model**.
    2.  Receives Location -> Sends to **Open-Meteo API**.
    3.  Combines `(Emotion + Weather + Time)` -> Sends to **Groq API**.
    4.  Receives Song List -> Sends to **yt-dlp**.
    5.  Streams Audio -> Sends to **Frontend**.

### 2.3 AI & Data Processing
* **Vision Model (RMN):**
    * *Input:* Raw image frame.
    * *Logic:* Residual Masking Network for facial affect recognition.
    * *Output:* Emotion label (Happy, Sad, Neutral, Angry, etc.).
* **LLM Curation (Groq Llama-3):**
    * *Input Prompt:* "User is [Emotion] on a [Weather] [Time of Day]. Suggest 5 songs."
    * *Hardware:* Groq LPU (Language Processing Unit) for ultra-low latency.
* **Mood Stabilizer Algorithm:**
    * Buffer size: 5 Frames.
    * Logic: `Mode(Last_5_Frames)` is used as the trigger to prevent flickering emotions.

---

## 3. Data Flow Diagram

1.  **User** grants camera/location access.
2.  **Frontend** sends `Frame + Coords` -> **Backend** (via WebSocket).
3.  **Backend** calls **Open-Meteo** -> Returns `Weather_Data`.
4.  **Backend** feeds `Frame` -> **RMN Model** -> Returns `Emotion_Label`.
5.  **Backend** checks `Stability_Buffer`. If stable:
6.  **Backend** constructs Prompt -> **Groq API** -> Returns `Song_List`.
7.  **Backend** searches `Song_List` in **yt-dlp** -> Returns `Audio_URL`.
8.  **Frontend** receives `Audio_URL` & `Theme_Color` -> Plays Music & Updates UI.

---

## 4. Database Schema (Future Implementation)
*Note: Current version is stateless. Future version using MongoDB.*

**Collection: UserSessions**
```json
{
  "user_id": "uuid",
  "timestamp": "ISO8601",
  "detected_mood": "Sad",
  "context": {
    "weather": "Rainy",
    "time": "Night"
  },
  "songs_played": ["Song A", "Song B"],
  "user_feedback": "Skipped"
}
