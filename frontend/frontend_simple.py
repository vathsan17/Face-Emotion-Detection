import streamlit as st
import cv2
import numpy as np
from rmn import RMN

# --- 1. SETUP ---
st.set_page_config(page_title="Emotion Detector", layout="wide")
st.title("👁️ AI Emotion Scanner")

# Load the AI Brain (Cached so it doesn't reload every frame)
@st.cache_resource
def load_ai_model():
    return RMN()

model = load_ai_model()

# --- 2. LAYOUT ---
# Left: The Camera Feed
# Right: The Huge Emotion Text
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown("### Live Camera")
    video_placeholder = st.empty()

with col2:
    st.markdown("### Detected Emotion")
    emotion_text = st.empty()
    confidence_bar = st.empty()

# --- 3. THE LOOP ---
cap = cv2.VideoCapture(0)
stop_button = st.button("Stop Scanner")

while cap.isOpened() and not stop_button:
    ret, frame = cap.read()
    if not ret:
        st.error("Camera not accessible.")
        break

    # Detect Emotion
    results = model.detect_emotion_for_single_frame(frame)

    # Defaults (When no face is seen)
    mood = "Scanning..."
    conf = 0
    color = (200, 200, 200) # Grey

    # If face detected
    if results:
        face = results[0]
        mood = face['emo_label'].upper()
        conf = face['emo_proba'] # 0.0 to 1.0
        
        # Draw Green Box on the video
        cv2.rectangle(frame, (face['xmin'], face['ymin']), 
                      (face['xmax'], face['ymax']), (0, 255, 0), 3)

    # --- UPDATE UI ---
    
    # 1. Update The Video (Left Side)
    # Convert BGR (OpenCV) to RGB (Screen)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_placeholder.image(frame, channels="RGB")

    # 2. Update The Text (Right Side)
    # We use HTML to make the text HUGE and readable
    with emotion_text.container():
        st.markdown(f"""
            <div style='text-align: center;'>
                <h1 style='font-size: 60px; color: #4CAF50;'>{mood}</h1>
                <h3>Confidence: {int(conf * 100)}%</h3>
            </div>
            """, unsafe_allow_html=True)
            
    # Simple progress bar for confidence
    confidence_bar.progress(conf)

cap.release()