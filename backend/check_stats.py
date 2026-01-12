import pymongo
from datetime import datetime

# Connect
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mooddj_db"]

print("--- 📊 MOODDJ DATABASE REPORT ---")

# 1. Check Songs
song_count = db.songs.count_documents({})
print(f"🎵 Total Songs in Inventory: {song_count}")

# 2. Check History
print(f"\n--- 🕒 Recent History (Last 5) ---")
history = db.history.find().sort("timestamp", -1).limit(5)
for h in history:
    print(f"[{h['timestamp'].strftime('%H:%M:%S')}] User was {h['mood_detected']} -> Played: {h['song_title']}")

# 3. Check Likes
print(f"\n--- ❤️ Liked Songs ---")
likes = db.likes.find()
for l in likes:
    print(f"⭐ {l['song_title']} (Liked when {l['mood_context']})")

print("\n-------------------------------")