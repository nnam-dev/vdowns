import yt_dlp
from pathlib import Path

file_path = Path('static/cookies.txt')

if file_path.is_file():
    print("The file exists.")
else:
    print("The file does not exist.")

# Options to use the manually exported cookies
ydl_opts = {
    'cookies': 'static/cookies.txt',  # Full path to the exported cookies.txt file
}

url = 'https://www.youtube.com/shorts/YV-gwsg2Ekc'

# Attempt to download the video using the exported cookies
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])
