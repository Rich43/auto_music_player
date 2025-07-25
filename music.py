import subprocess
import yt_dlp
import random
import sys
import re

# Playlist of track titles (as strings)
track_titles = [
    "Phuture – Acid Tracks",
    "Hardfloor – Acperience 1",
    "DJ Pierre – Box Energy",
    "Josh Wink – Higher State of Consciousness",
    "Joey Beltram – Energy Flash",
    "CJ Bolland – Camargue",
    "Surgeon – Magneze",
    "Jeff Mills – The Bells",
    "Sven Väth – L'Esperanza",
    "Jam & Spoon – Stella",
    "Age of Love – The Age of Love",
    "Push – Universal Nation",
    "Binary Finary – 1998 Paul van Dyk Remix",
    "Veracocha – Carte Blanche",
    "Rotterdam Terror Corps – Rotterdam Hooligan",
    "Neophyte – Braincracking",
    "3 Steps Ahead – Drop It",
    "Charly Lownoise & Mental Theo – Wonderful Days",
    "L.A. Style – James Brown Is Dead",
    "Orbital – Halcyon + On + On",
    "The Orb – Little Fluffy Clouds",
    "Aphex Twin – Xtal",
    "Autechre – Eggshell",
    "Global Communication – 14:31",
    "2 Unlimited – Get Ready For This",
    "Snap! – Rhythm Is A Dancer",
    "Technotronic – Pump Up The Jam",
    "La Bouche – Be My Lover",
    "Culture Beat – Mr. Vain",
    "The Prodigy – Your Love",
    "Altern 8 – Activ 8 (Come With Me)",
    "Shut Up and Dance – Raving I'm Raving",
    "Omni Trio – Renegade Snares",
    "LTJ Bukem – Horizons"
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
