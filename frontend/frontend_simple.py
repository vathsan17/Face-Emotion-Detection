import streamlit as st
import cv2
import numpy as np
from rmn import RMN
import collections
import streamlit.components.v1 as components
import pyttsx3
import threading
import keyboard
import time
import pymongo
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MoodDJ v3 - Stable", layout="wide", page_icon="Hz")

# Custom CSS
st.markdown("""
<style>
    .stApp { background-color: #121212; color: white; }
    div.stButton > button {
        background-color: #1DB954; color: white; border-radius: 20px; border: none;
        padding: 10px 24px; font-weight: bold; text-transform: uppercase; width: 100%;
    }
    div.stButton > button:hover { background-color: #1ed760; color: black; }
    .quote-box {
        background-color: #282828; padding: 20px; border-radius: 10px;
        text-align: center; margin-bottom: 20px; font-style: italic; border-left: 5px solid #1DB954;
    }
    h1, h2, h3, p { font-family: sans-serif; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATABASE & STATE ---
@st.cache_resource
def init_db():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["mooddj_db"]
        db.command('ping')
        return db
    except:
        return None

db = init_db()

# Initialize Session State
if 'current_track_index' not in st.session_state: st.session_state.current_track_index = 0
if 'scanning' not in st.session_state: st.session_state.scanning = True
if 'locked_emotion' not in st.session_state: st.session_state.locked_emotion = None
if 'emotion_buffer' not in st.session_state: st.session_state.emotion_buffer = []
if 'session_logged' not in st.session_state: st.session_state.session_logged = False
if 'rerun_trigger' not in st.session_state: st.session_state.rerun_trigger = False

# --- 3. HELPER FUNCTIONS ---
def get_music_for_mood(mood):
    if db is None: return [], [], "Database Error - Check MongoDB"
    songs = list(db.songs.find({"mood": mood}))
    if not songs: songs = list(db.songs.find({"mood": "neutral"}))
    if not songs: return [], [], "No songs found in DB."
    
    track_ids = [s['spotify_id'] for s in songs]
    quote = songs[0]['quote']
    return songs, track_ids, quote

def log_history(mood, song_data):
    if db is not None:
        db.history.insert_one({
            "user_id": "guest", 
            "mood_detected": mood, 
            "song_title": song_data.get('title'),
            "spotify_id": song_data.get('spotify_id'),
            "timestamp": datetime.now()
        })

def save_like(mood, song_data):
    if db is None: return False
    exists = db.likes.find_one({"user_id": "guest", "spotify_id": song_data['spotify_id']})
    if not exists:
        db.likes.insert_one({
            "user_id": "guest",
            "song_title": song_data.get('title'),
            "artist": song_data.get('artist'),
            "spotify_id": song_data['spotify_id'],
            "mood_context": mood,
            "timestamp": datetime.now()
        })
        return True
    return False

def speak(text):
    def _speak():
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except: pass
    threading.Thread(target=_speak, daemon=True).start()

@st.cache_resource
def load_ai_model():
    return RMN()
model = load_ai_model()

# --- 4. STATIC UI LAYOUT (Built ONCE) ---
st.title("🎧 MoodDJ: AI Spotify Controller")
st.caption("Controls: [Space Hold]=Rescan | [Space x2]=Next | [Space x3]=Prev | [L]=Like Song ❤️ | [Q]=Quit")

# Create the main layout columns
col1, col2 = st.columns([1.5, 1])

# --- COLUMN 1: LIVE FEED ---
with col1:
    st.markdown("### 📷 Live Feed")
    # We create empty containers that we will update in the loop
    video_container = st.empty()
    progress_container = st.empty()
    status_container = st.empty()

# --- COLUMN 2: PLAYER & CONTROLS ---
with col2:
    st.markdown("### 🎵 Now Playing")
    
    # 1. Quote Section
    quote_container = st.empty()
    
    # 2. Player Section
    player_container = st.empty()
    
    # 3. Manual Controls (These trigger re-runs automatically)
    c1, c2, c3 = st.columns(3)
    with c1:
        if st.button("⏮ Prev"):
            if st.session_state.locked_emotion:
                st.session_state.current_track_index -= 1
                st.rerun()
    with c2:
        if st.button("🔄 Re-Scan"):
            st.session_state.scanning = True
            st.session_state.locked_emotion = None
            st.session_state.emotion_buffer = []
            st.session_state.current_track_index = 0
            st.session_state.session_logged = False
            st.rerun()
    with c3:
        if st.button("Next ⏭"):
            if st.session_state.locked_emotion:
                st.session_state.current_track_index += 1
                st.rerun()

# --- 5. RENDER LOCKED STATE (Pre-Loop) ---
# This ensures the player stays visible even if the camera loop crashes or pauses
if st.session_state.locked_emotion:
    mood = st.session_state.locked_emotion
    song_objects, track_ids, quote = get_music_for_mood(mood)
    
    if song_objects:
        idx = st.session_state.current_track_index % len(song_objects)
        current_song = song_objects[idx]
        track_id = current_song['spotify_id']
        
        # Log History Once
        if not st.session_state.session_logged:
            log_history(mood, current_song)
            st.session_state.session_logged = True
            
        # Render Quote
        quote_container.markdown(f"""
        <div class="quote-box">
            <h3>{mood.upper()}</h3>
            <p>"{quote}"</p>
            <small>Now Playing: {current_song['title']} - {current_song['artist']}</small>
        </div>
        """, unsafe_allow_html=True)
        
        # Render Spotify Player (Official Embed URL)
        with player_container:
            components.html(
                f'<iframe style="border-radius:12px" src="https://open.spotify.com/embed/track/{track_id}?utm_source=generator" width="100%" height="152" frameBorder="0" allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" loading="lazy"></iframe>',
                height=160
            )
            
        status_container.success(f"✅ Mood Locked: {mood.title()}")

# --- 6. VIDEO PROCESSING LOOP ---
cap = cv2.VideoCapture(0)

# Keyboard State Vars
if 'key_state' not in st.session_state:
    st.session_state.key_state = {"space_pressed": False, "start_time": 0, "tap_count": 0, "last_tap": 0}

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: 
        status_container.error("Camera not detected.")
        break
    
    # --- AI SCANNING LOGIC ---
    if st.session_state.scanning:
        # Detect
        results = model.detect_emotion_for_single_frame(frame)
        if results:
            face = results[0]
            st.session_state.emotion_buffer.append(face['emo_label'])
            # Draw Box
            cv2.rectangle(frame, (face['xmin'], face['ymin']), (face['xmax'], face['ymax']), (0, 255, 0), 2)
            cv2.putText(frame, face['emo_label'].upper(), (face['xmin'], face['ymin']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255,0), 2)
        
        # Progress Bar logic
        frames_needed = 15
        prog = min(len(st.session_state.emotion_buffer) / frames_needed, 1.0)
        progress_container.progress(prog)
        
        # Lock Logic
        if len(st.session_state.emotion_buffer) >= frames_needed:
            c = collections.Counter(st.session_state.emotion_buffer)
            mood = c.most_common(1)[0][0]
            
            st.session_state.locked_emotion = mood
            st.session_state.scanning = False
            speak(f"You look {mood}. Playing music.")
            st.rerun() # Exit loop and restart script to render player

    # --- DISPLAY FRAME ---
    # Convert BGR to RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_container.image(frame_rgb, channels="RGB")

    # --- KEYBOARD CONTROLS ---
    # We use a localized state dict to avoid session_state lag inside high-speed loop
    ks = st.session_state.key_state
    current_time = time.time()

    # 1. Like Song (L)
    if keyboard.is_pressed('l'):
        if st.session_state.locked_emotion and 'song_objects' in locals():
            idx = st.session_state.current_track_index % len(song_objects)
            saved = save_like(st.session_state.locked_emotion, song_objects[idx])
            if saved:
                speak("Added to favorites")
                st.toast(f"❤️ Liked: {song_objects[idx]['title']}")
            time.sleep(0.5) # Debounce

    # 2. Quit (Q)
    if keyboard.is_pressed('q'):
        cap.release()
        st.stop()

    # 3. Space Bar (Nav & Rescan)
    if keyboard.is_pressed('space'):
        if not ks["space_pressed"]:
            ks["space_pressed"] = True
            ks["start_time"] = current_time
    else:
        if ks["space_pressed"]: # Just Released
            ks["space_pressed"] = False
            duration = current_time - ks["start_time"]
            
            if duration > 0.8: # HOLD (> 0.8s) -> RESCAN
                speak("Rescanning")
                st.session_state.scanning = True
                st.session_state.locked_emotion = None
                st.session_state.emotion_buffer = []
                st.session_state.session_logged = False
                cap.release()
                st.rerun()
            else: # TAP
                ks["tap_count"] += 1
                ks["last_tap"] = current_time

    # Process Taps (Debounce 0.4s)
    if ks["tap_count"] > 0 and (current_time - ks["last_tap"] > 0.4):
        if ks["tap_count"] == 2: # Double Tap -> Next
            st.session_state.current_track_index += 1
            cap.release()
            st.rerun()
        elif ks["tap_count"] == 3: # Triple Tap -> Prev
            st.session_state.current_track_index -= 1
            cap.release()
            st.rerun()
        ks["tap_count"] = 0
    
    # Save back to session state
    st.session_state.key_state = ks

    # Small sleep to save CPU
    time.sleep(0.01)

cap.release()