import streamlit as st
import pymongo
import pandas as pd
import plotly.express as px
from datetime import datetime

# --- 1. CONFIGURATION ---
st.set_page_config(page_title="MoodDJ Analytics", layout="wide", page_icon="📊")

# Custom CSS for Dark Mode "Product" Feel
st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: white; }
    .metric-card {
        background-color: #262730;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #1DB954;
        text-align: center;
    }
    h1, h2, h3 { color: #1DB954; }
</style>
""", unsafe_allow_html=True)

# --- 2. DATABASE CONNECTION ---
@st.cache_resource
def init_db():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client["mooddj_db"]
    except:
        return None

db = init_db()

# --- 3. DATA FETCHING ---
def get_data():
    if db is None: return None, None
    
    # Fetch History
    history_cursor = db.history.find().sort("timestamp", -1)
    df_history = pd.DataFrame(list(history_cursor))
    
    # Fetch Likes
    likes_cursor = db.likes.find().sort("timestamp", -1)
    df_likes = pd.DataFrame(list(likes_cursor))

    return df_history, df_likes

# --- 4. DASHBOARD UI ---
st.title("📊 MoodDJ Dashboard")
st.markdown("Real-time analytics of your listening habits and mood.")

if st.button("🔄 Refresh Data"):
    st.rerun()

df_history, df_likes = get_data()

if df_history is not None and not df_history.empty:
    
    # --- A. KPI ROW (Key Metrics) ---
    col1, col2, col3 = st.columns(3)
    
    total_sessions = len(df_history)
    top_mood = df_history['mood_detected'].mode()[0] if not df_history.empty else "N/A"
    total_likes = len(df_likes) if df_likes is not None else 0

    with col1:
        st.markdown(f'<div class="metric-card"><h3>{total_sessions}</h3><p>Total Sessions</p></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><h3>{top_mood.title()}</h3><p>Dominant Mood</p></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><h3>{total_likes}</h3><p>Liked Songs ❤️</p></div>', unsafe_allow_html=True)

    st.markdown("---")

    # --- B. CHARTS ROW ---
    c1, c2 = st.columns([2, 1])

    with c1:
        st.subheader("📈 Mood Trends (Last 50)")
        # Clean timestamp for chart
        if 'timestamp' in df_history.columns:
            # Simple bar chart of mood counts
            mood_counts = df_history['mood_detected'].value_counts().reset_index()
            mood_counts.columns = ['Mood', 'Count']
            
            fig = px.bar(mood_counts, x='Mood', y='Count', color='Mood', 
                         color_discrete_sequence=px.colors.qualitative.Pastel,
                         template="plotly_dark")
            st.plotly_chart(fig, use_container_width=True)

    with c2:
        st.subheader("🥧 Mood Distribution")
        fig_pie = px.pie(mood_counts, values='Count', names='Mood', hole=0.4,
                         template="plotly_dark")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown("---")

    # --- C. DATA TABLES ---
    t1, t2 = st.columns(2)

    with t1:
        st.subheader("🕒 Recent History")
        # Show specific columns to keep it clean
        if not df_history.empty:
            display_hist = df_history[['timestamp', 'mood_detected', 'song_title']].head(10)
            st.dataframe(display_hist, hide_index=True, use_container_width=True)

    with t2:
        st.subheader("❤️ Your Liked Songs")
        if df_likes is not None and not df_likes.empty:
            display_likes = df_likes[['song_title', 'artist', 'mood_context']].head(10)
            st.dataframe(display_likes, hide_index=True, use_container_width=True)
        else:
            st.info("No liked songs yet. Go to the app and press 'L'!")

else:
    st.warning("⚠️ No data found in Database. Run the main app and listen to some music first!")