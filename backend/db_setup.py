import pymongo

# 1. Connect to MongoDB (Local)
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["mooddj_db"]

# 2. Define Collections
songs_col = db["songs"]
history_col = db["history"]
likes_col = db["likes"]

# 3. Your Initial Data (The 'Seed')
music_data = [
    # HAPPY
    {"mood": "happy", "spotify_id": "60nZcImufyMA1KT4e0pksA", "title": "Happy", "artist": "Pharrell Williams", "quote": "Don't worry, be happy! ☀️"},
    {"mood": "happy", "spotify_id": "1WkMMvw4IGtp084Q3eTPQ", "title": "Can't Stop The Feeling", "artist": "Justin Timberlake", "quote": "Don't worry, be happy! ☀️"},
    {"mood": "happy", "spotify_id": "32OlwWuMpZ6b0aN2RZOeMS", "title": "Uptown Funk", "artist": "Bruno Mars", "quote": "Don't worry, be happy! ☀️"},
    
    # SAD
    {"mood": "sad", "spotify_id": "4kflIGfjdZJW4ot2ioixTB", "title": "Someone Like You", "artist": "Adele", "quote": "Tough times never last, but tough people do. 💪"},
    {"mood": "sad", "spotify_id": "4y1LsJpmMti1ii5Tp2NrRk", "title": "All of Me", "artist": "John Legend", "quote": "Tough times never last, but tough people do. 💪"},
    {"mood": "sad", "spotify_id": "2BJxxw9kPprtuCvYZ6M1x5", "title": "Let Her Go", "artist": "Passenger", "quote": "Tough times never last, but tough people do. 💪"},

    # ANGRY
    {"mood": "angry", "spotify_id": "60a0Rd6pjrkxjPbaKzXjfq", "title": "In the End", "artist": "Linkin Park", "quote": "Take a deep breath. You got this. 🧘"},
    {"mood": "angry", "spotify_id": "5cZqsjVs6MevCnAkasbEOX", "title": "Break Stuff", "artist": "Limp Bizkit", "quote": "Take a deep breath. You got this. 🧘"},
    {"mood": "angry", "spotify_id": "2zYzyRzz6pRmhPzyfMEC8s", "title": "Highway to Hell", "artist": "AC/DC", "quote": "Take a deep breath. You got this. 🧘"},

    # NEUTRAL
    {"mood": "neutral", "spotify_id": "0VjIjW4GlUZAMYd2vXMi3b", "title": "Blinding Lights", "artist": "The Weeknd", "quote": "Peace begins with a smile. 🍃"},
    {"mood": "neutral", "spotify_id": "75FpbthrwQkTAPh6leKLn4", "title": "River Flows in You", "artist": "Yiruma", "quote": "Peace begins with a smile. 🍃"},
    {"mood": "neutral", "spotify_id": "6kkwzB6hXLIONkEk9JciA6", "title": "Weightless", "artist": "Marconi Union", "quote": "Peace begins with a smile. 🍃"},

    # SURPRISE
    {"mood": "surprise", "spotify_id": "3z8h0TU7ReDPLIbEnYhWzb", "title": "Bohemian Rhapsody", "artist": "Queen", "quote": "Life is full of surprises! 🎉"},
    {"mood": "surprise", "spotify_id": "2xLMifQCjDGFmkHkpNLD9h", "title": "Sicko Mode", "artist": "Travis Scott", "quote": "Life is full of surprises! 🎉"},
    {"mood": "surprise", "spotify_id": "2b9lp5c6CQQKJJH6y4isUW", "title": "Thunderstruck", "artist": "AC/DC", "quote": "Life is full of surprises! 🎉"},

    # FEAR
    {"mood": "fear", "spotify_id": "5sICkBXVmaCQk5aISGR3x1", "title": "Enter Sandman", "artist": "Metallica", "quote": "Courage is being scared but doing it anyway. 🛡️"},
    {"mood": "fear", "spotify_id": "3Hw94iF11gK7D5oZJj4z29", "title": "Thriller", "artist": "Michael Jackson", "quote": "Courage is being scared but doing it anyway. 🛡️"},
    {"mood": "fear", "spotify_id": "4jXl6VtkFFKIt3cYpyhWg9", "title": "Immigrant Song", "artist": "Led Zeppelin", "quote": "Courage is being scared but doing it anyway. 🛡️"},

    # DISGUST
    {"mood": "disgust", "spotify_id": "2Fxmhks0bxGSBdJ92vM42m", "title": "Bad Guy", "artist": "Billie Eilish", "quote": "Shake it off and keep moving. 🌪️"},
    {"mood": "disgust", "spotify_id": "6I9VzXrHxO9rA9A5euc8Ak", "title": "Toxicity", "artist": "System of a Down", "quote": "Shake it off and keep moving. 🌪️"},
    {"mood": "disgust", "spotify_id": "7GHyHgxH5PN9a8F46261c3", "title": "Humble", "artist": "Kendrick Lamar", "quote": "Shake it off and keep moving. 🌪️"},
]

# 4. Clear existing data (Optional, safer for testing)
songs_col.delete_many({})
print("🧹 Old data cleared.")

# 5. Insert New Data
songs_col.insert_many(music_data)
print(f"✅ Successfully inserted {len(music_data)} songs into 'mooddj_db'.")