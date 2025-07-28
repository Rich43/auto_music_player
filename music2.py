import subprocess
import yt_dlp
import random
import sys
import re

# Playlist of track titles (as strings)
track_titles = [
    "Silence – Delerium (DJ Tiësto's In Search of Sunrise Remix)",
    "Airwave – Rank 1",
    "Seven Cities – Solarstone's Atlantis Mix",
    "Carte Blanche – Veracocha",
    "Life Less Ordinary – Alex M.O.R.P.H. Original Mix",
    "Out of the Blue – System F Original Extended",
    "Twisted – Svenson & Gielen",
    "Airtight – Max Graham",
    "Sacred (Dub) – Sander Kleinenberg",
    "10 in 01 – Members of Mayday (Paul van Dyk Club Mix)",
    "Positron – Cygnus X (Armin van Buuren Remix)",
    "Finished Symphony – Hybrid (Echoplex Remix)",
    "Café Del Mar – Energy 52 (Nalin & Kane Remix)",
    "Stimulated – Marco V",
    "Clear Blue Water – OceanLab",
    "Happiness Happening – Lost Witness",
    "Fly Away – Vincent de Moor",
    "Time Is the Healer – Riva (Original Vocal Mix)",
    "Everytime – Lustral (Nalin & Kane Remix)",
    "Lemon Tree – Marcel Woods",
    "Liquidation – Liquid DJ Team (Marco V Remix)",
    "Sosei – Airscape",
    "Deadline – Dutch Force",
    "Anomaly (Calling Your Name) – Libra Presents Taylor (Ferry Corsten Remix)"
]

SHUFFLE = True
NUM_RESULTS = 8

def tokenize(text):
    return set(re.findall(r'\w+', text.lower()))

def match_score(query, title):
    query_tokens = tokenize(query)
    title_tokens = tokenize(title)
    return len(query_tokens & title_tokens)

def search_youtube_best_match(query):
    ydl_opts = {
        'quiet': True,
        'default_search': f'ytsearch{NUM_RESULTS}',
        'format': 'bestaudio[ext=m4a]/bestaudio/best',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        search_result = ydl.extract_info(query, download=False)
        entries = search_result['entries']

        best = max(entries, key=lambda e: match_score(query, e.get('title', '')))
        return best['url'], best.get('title', 'Unknown Title')

def play_audio(query):
    try:
        url, title = search_youtube_best_match(query)
        print(f"\n🎶 Now Playing: {title}")
        subprocess.run(["mpv", "--no-video", url])
    except Exception as e:
        print(f"⚠️ Error playing {query}: {e}")

def main():
    print("🔊 90s Rave Player with Smart Matching 🔊\n")

    queue = track_titles.copy()
    if SHUFFLE:
        random.shuffle(queue)

    try:
        for track in queue:
            play_audio(track)
    except KeyboardInterrupt:
        print("\n👋 Party over. See you next drop.")
        sys.exit(0)

if __name__ == "__main__":
    main()
