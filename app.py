import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify credentials from Streamlit secrets
CLIENT_ID = st.secrets["CLIENT_ID"]
CLIENT_SECRET = st.secrets["CLIENT_SECRET"]
REDIRECT_URI = st.secrets["REDIRECT_URI"]

# Spotify client with necessary scopes
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope="user-read-playback-state user-modify-playback-state user-read-currently-playing"
))

st.set_page_config(page_title="🎧 Music App", layout="centered")
st.title("🎶 Streamlit Music App (Fast & Smooth)")

# 🚀 Cached search to boost speed
@st.cache_data(ttl=300)
def search_tracks(query):
    results = sp.search(q=query, type="track", limit=5)
    return results["tracks"]["items"]

# Search box
query = st.text_input("Search for a song, artist, or album:")

if query:
    tracks = search_tracks(query)

    if tracks:
        track_names = [f"{t['name']} - {t['artists'][0]['name']}" for t in tracks]
        track_uris = [t["uri"] for t in tracks]
        album_arts = [t["album"]["images"][0]["url"] for t in tracks]

        selected_index = st.selectbox("Choose a track:", range(len(track_names)), format_func=lambda i: track_names[i])
        
        st.image(album_arts[selected_index], width=200)

        if st.button("▶️ Play Selected Track"):
            try:
                sp.start_playback(uris=[track_uris[selected_index]])
                st.success("✅ Playback started — make sure your Spotify app is open.")
            except spotipy.exceptions.SpotifyException as e:
                st.error("⚠️ Playback failed. Please ensure your Spotify app is open and you're logged in.")

    else:
        st.warning("No tracks found for your search.")
