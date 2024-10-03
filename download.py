import os
import yt_dlp

def download_dash_video(youtube_url, output_dir):
    # Ensure the output directory exists or create it
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
            print(f"Created directory: {output_dir}")
    except Exception as e:
        print(f"Error creating directory {output_dir}: {e}")
        return

    cookies_path = '/full/path/to/cookies.txt'

    # yt-dlp options to download best video and audio streams separately
    ydl_opts = {
        'cookies': cookies_path,
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',  # Download best video and audio streams with specified formats
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Output filename template
        'merge_output_format': 'mp4',  # Final format after merging
        'restrictfilenames': True,  # Remove special characters in filenames
        'windowsfilenames': True,  # Ensure Windows-compatible filenames
        'postprocessors': [{
            'key': 'FFmpegMerger',  # Merges video and audio
        }],
        'verbose': True,  # Enable verbose output to help diagnose issues
       
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
        print(f"Video downloaded and merged in: {output_dir}")
    except Exception as e:
        print(f"Error downloading video: {e}")

# Example usage
youtube_url = 'https://youtube.com/shorts/2ON2kzUnoxA?si=0LfjdoQB7vu17rPl'  # Replace with actual YouTube video URL
output_dir = './downloads'  # Output directory

download_dash_video(youtube_url, output_dir)
