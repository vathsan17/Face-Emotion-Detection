import streamlit as st
import cv2
import numpy as np
from deepface import DeepFace
from PIL import Image

# --- 1. THE MOCK SPOTIFY SYSTEM (Since API is down) ---
class MockSpotify:
    """
    This class pretends to be the Spotify API. 
    It returns real song data structures so your logic stays valid.
    """
    def __init__(self):
        # We pre-fill this with some "fake" database songs
        self.mock_db = {
            "happy": {
                "name": "Happy",
                "artist": "Pharrell Williams",
                "cover": "https://i.scdn.co/image/ab67616d0000b273fff961962d3a373b5220c156",
                "link": "https://open.spotify.com/track/60nZcImufyMA1KT4eoro2W"
            },
            "sad": {
                "name": "Someone Like You",
                "artist": "Adele",
                "cover": "https://i.scdn.co/image/ab67616d0000b2732118bf9b198b05a95ded6300",
                "link": "https://open.spotify.com/track/4kflIGfjdZJW4ot2ioixTB"
            },
            "angry": {
                "name": "Break Stuff",
                "artist": "Limp Bizkit",
                "cover": "https://i.scdn.co/image/ab67616d0000b273b52d9a9307c08b47e2311693",
                "link": "https://open.spotify.com/track/5cZqsjVs6MevCnAkasbEOX"
            },
            "neutral": {
                "name": "Weightless",
                "artist": "Marconi Union",
                "cover": "https://i.scdn.co/image/ab67616d0000b27376c95350486c12567c824c26",
                "link": "https://open.spotify.com/track/6kkwzB6hXLIONkEk9JciA6"
            },
            "surprise": {
                "name": "Bohemian Rhapsody",
                "artist": "Queen",
                "cover": "https://i.scdn.co/image/ab67616d0000b273e8b066f70c206551210d902b",
                "link": "https://open.spotify.com/track/3z8h0TU7NB750qJyF7RIvx"
            }
        }

    def recommend(self, emotion):
        # Default to 'neutral' if emotion isn't in our DB
        data = self.mock_db.get(emotion, self.mock_db['neutral'])
        return data

# Initialize our Fake AI DJ
dj = MockSpotify()

# --- 2. THE UI & LOGIC ---
st.title("🎵 MoodMatcher (Hackathon Demo)")
st.write("Detects your facial expression and recommends a song.")

# Create two columns for layout
col1, col2 = st.columns(2)

with col1:
    st.header("Your Face")
    # Streamlit's camera input is the easiest way to handle video
    img_file_buffer = st.camera_input("Take a picture")

with col2:
    st.header("The Recommendation")
    
    if img_file_buffer is not None:
        # Convert the image to a format OpenCV can read
        bytes_data = img_file_buffer.getvalue()
        cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

        try:
            with st.spinner("Analyzing your mood..."):
                # Use DeepFace to detect emotion
                # enforce_detection=False allows it to work even if face is blurry
                result = DeepFace.analyze(cv2_img, actions=['emotion'], enforce_detection=False)
                
                # Get the dominant emotion
                emotion = result[0]['dominant_emotion']
                st.success(f"Detected Mood: **{emotion.upper()}**")
                
                # GET SONG (From our Mock DJ)
                song = dj.recommend(emotion)
                
                # Display Result
                st.image(song['cover'], width=300)
                st.markdown(f"### {song['name']}")
                st.markdown(f"**Artist:** {song['artist']}")
                st.markdown(f"[Listen on Spotify]({song['link']})")

        except Exception as e:
            st.error(f"Could not detect face. Try again! (Error: {e})")
    else:
        st.info("Waiting for camera input...")