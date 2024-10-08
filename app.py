import io
import json
import os

from flask import Flask, render_template, request, jsonify, send_file, url_for, Response, stream_with_context
from urllib.parse import quote
import yt_dlp
import requests
from moviepy.editor import VideoFileClip, AudioFileClip
import tempfile
import subprocess

app = Flask(__name__)


# Helper functions for video information fetching



def fetch_youtube_info(url):
    # Placeholder for fetching Instagram video information
    # Implement API or web scraping here
    # Placeholder for fetching Facebook video information
    # Implement API or web scraping here
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,
        'cookiesfrombrowser': 'chrome',
    }
    defined_keys = 'manifest_url'
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

    # Audio Format URL Formatting
    audio_format = [f for f in formats if f.get('audio_ext') == "mp4" and f.get('video_ext') == "none"]

    f_audio_format = audio_format[0]
    f_audio_format_url = f_audio_format['url']

    # Extract necessary video details
    video_details = {
        'title': info_dict.get('title', 'Unknown Title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'duration': info_dict.get('duration', 0),
    }

    # Filter formats for MP4 only
    mp4_formats = [
        {
            'format_id': f['format_id'],
            'format': f"{f['width']}x{f['height']}",
            'quality': '',
            'url': f['url'],

        }
        for f in formats if f.get('ext') == 'mp4' and f.get('video_ext') != "none" and defined_keys not in f
    ]
    mp4s = [f for f in formats if f.get('ext') == 'mp4' and f.get('video_ext') != "none" and defined_keys not in f]

    print(
        json.dumps(mp4s)
    )
    # Best Format
    best_format = max(mp4_formats, key=lambda f: f['format'])

    print(best_format['url'])

    return {
        'title': info_dict.get('title', 'Unknown Title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'duration': info_dict.get('duration', 0),
        'formats': mp4_formats,
        'best': best_format['url'],
        'audio': f_audio_format_url

    }


def download_dash_video(youtube_url, output_dir):
    # Ensure the output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # yt-dlp options to download best video and audio streams separately
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # Download best video and audio streams
         'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),  # Output filename template
        'merge_output_format': 'mp4',  # Final format after merging
        'postprocessors': [{
            'key': 'FFmpegMerger',  # Merges video and audio
        }],
        'restrictfilenames': True,  # Remove special characters in filenames
        'windowsfilenames': True,  # Ensure Windows-compatible filenames
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Merged file will be saved in the output_dir with the video title as its name


def fetch_facebook_info(url):
    # Placeholder for fetching Facebook video information
    # Implement API or web scraping here
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

        # Extract necessary video details
        video_details = {
            'title': info_dict.get('title', 'Unknown Title'),
            'thumbnail': info_dict.get('thumbnail', ''),
            'duration': info_dict.get('duration', 0),
        }

        # Filter formats for MP4 only
        mp4_formats = [
            {
                'format_id': f['format_id'],
                'format': f['format'],
                'quality': '',
                'url': f['url'],
            }
            for f in formats if f.get('ext') == 'mp4' and f.get('manifest_url') is None
        ]

        best_formats = [
            f for f in formats if ('hd' in f.get('format'))
        ]
        f_best_format = best_formats[0]

        print(f_best_format.get('url'))

    return {
        'title': info_dict.get('title', 'Unknown Title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'duration': info_dict.get('duration', 0),
        'formats': mp4_formats,
        'best': f_best_format.get('url')
    }


def fetch_instagram_info(url):
    # Placeholder for fetching Instagram video information
    # Implement API or web scraping here
    # Placeholder for fetching Facebook video information
    # Implement API or web scraping here
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

    # Audio Format URL Formatting
    audio_format = [f for f in formats if f.get('acodec') != "none" and f.get('vcodec') == "none"]
    f_audio_format = audio_format[0]
    f_audio_format_url = f_audio_format['url']

    # Extract necessary video details
    video_details = {
        'title': info_dict.get('title', 'Unknown Title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'duration': info_dict.get('duration', 0),
    }

    # Filter formats for MP4 only
    mp4_formats = [
        {
            'format_id': f['format_id'],
            'format': f"{f['width']}x{f['height']}",
            'quality': '',
            'url': f['url'],

        }
        for f in formats if f.get('ext') == 'mp4'
    ]

    # Best Format
    best_format = max(mp4_formats, key=lambda f: f['format'])

    print(best_format['url'])

    return {
        'title': info_dict.get('title', 'Unknown Title'),
        'thumbnail': info_dict.get('thumbnail', ''),
        'duration': info_dict.get('duration', 0),
        'formats': mp4_formats,
        'best': best_format['url'],
        'audio': f_audio_format_url

    }


def fetch_tiktok_info(url):
    # Placeholder for fetching TikTok video information
    # Implement API or web scraping here

    # Placeholder for fetching Instagram video information
    # Implement API or web scraping here
    # Placeholder for fetching Facebook video information
    # Implement API or web scraping here
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'noplaylist': True,

    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
        formats = info_dict.get('formats', [])

        print(json.dumps(info_dict))

    return {
        'title': 'Sample TikTok Video',
        'thumbnail': 'https://via.placeholder.com/150',
        'duration': 60,
        'formats': [{'url': 'https://example.com/video.mp4', 'format': 'MP4', 'quality': 'High'}]
    }


def fetch_twitter_info(url):
    # Placeholder for fetching Twitter video information
    # Implement API or web scraping here
    return {
        'title': 'Sample Twitter Video',
        'thumbnail': 'https://via.placeholder.com/150',
        'duration': 45,
        'formats': [{'url': 'https://example.com/video.mp4', 'format': 'MP4', 'quality': 'High'}]
    }


def merge_video_audio(video_url, audio_url):
    # Fetch the video and audio streams in memory
    video_response = requests.get(video_url)
    audio_response = requests.get(audio_url)

    output_dir = './downloads'  # Output directory

    download_dash_video(video_url, output_dir)

    # Create temporary files to hold the video and audio streams
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as video_temp_file:
        video_temp_file.write(video_response.content)
        video_temp_file_path = video_temp_file.name  # Save the file path to delete later

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as audio_temp_file:
        audio_temp_file.write(audio_response.content)
        audio_temp_file_path = audio_temp_file.name  # Save the file path to delete later

    print(video_temp_file_path)

    # Use moviepy to load the video and audio files
    video_clip = VideoFileClip(video_temp_file_path)
    audio_clip = AudioFileClip(audio_temp_file_path)

    # Set the audio of the video to the audio clip
    video_with_audio = video_clip.set_audio(audio_clip)

    # Save the merged video to a new temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as output_temp_file:
        output_file_path = output_temp_file.name  # Save the output file path

    video_with_audio.write_videofile(output_file_path, codec="libx264", audio_codec="aac")

    # Close the video and audio clips to release the file handles
    video_clip.close()
    audio_clip.close()

    # Open the output file in memory
    with open(output_file_path, 'rb') as merged_video_file:
        merged_video = io.BytesIO(merged_video_file.read())

    # Cleanup: Remove temporary files
    os.remove(video_temp_file_path)
    os.remove(audio_temp_file_path)
    os.remove(output_file_path)

    # Return the merged video in memory
    merged_video.seek(0)
    return merged_video


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/<platform>')
def platform_page(platform):
    titles = {
        'youtube': 'YouTube Video Downloader',
        'facebook': 'Facebook Video Downloader',
        'instagram': 'Instagram Video Downloader',
        'tiktok': 'TikTok Video Downloader',
        'twitter': 'Twitter Video Downloader'
    }
    descriptions = {
        'youtube': 'Download YouTube videos in various formats including MP4.',
        'facebook': 'Download Facebook videos in various formats.',
        'instagram': 'Download Instagram videos in various formats.',
        'tiktok': 'Download TikTok videos in various formats.',
        'twitter': 'Download Twitter videos in various formats.'
    }
    images = {
        'youtube': 'img/youtube-thumbnail.jpg',
        'facebook': 'img/facebook-thumbnail.jpg',
        'instagram': 'img/instagram-thumbnail.jpg',
        'tiktok': 'img/tiktok-thumbnail.jpg',
        'twitter': 'img/twitter-thumbnail.jpg'
    }
    return render_template(
        'platform.html',
        platform=platform,
        title=titles.get(platform, 'Video Downloader'),
        description=descriptions.get(platform, 'Download videos from various platforms.'),
        keywords='video, download, ' + platform,
        og_title=titles.get(platform, 'Video Downloader'),
        og_description=descriptions.get(platform, 'Download videos from various platforms.'),
        og_image=url_for('static', filename=images.get(platform, 'img/og-image.jpg'))
    )


@app.route('/fetch_video_info', methods=['POST'])
def fetch_video_info_route():
    url = request.form.get('url')
    platform = request.form.get('platform')

    if not url or not platform:
        return jsonify({'error': 'URL and platform are required.'})

    try:
        if platform == 'youtube':
            info = fetch_youtube_info(url)
        elif platform == 'facebook':
            info = fetch_facebook_info(url)
        elif platform == 'instagram':
            info = fetch_instagram_info(url)
        elif platform == 'tiktok':
            info = fetch_tiktok_info(url)
        elif platform == 'twitter':
            info = fetch_twitter_info(url)
        else:
            return jsonify({'error': 'Unsupported platform.'})

        return jsonify(info)
    except Exception as e:
        return jsonify({'error': str(e)})


def download_video(url, platform, format_id=None, best=False):
    ydl_opts = {
        'format': 'bestaudio/best' if best else format_id,
        'merge_output_format': 'mp4',
        'outtmpl': 'temp_video.%(ext)s',  # Output to a temporary file
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp4',
            'preferredquality': '192',
        }, {
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        'progress_hooks': [lambda d: None]  # Avoid progress hooks interfering with stream
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        print(json.dumps(info))
        # Select best format if not specified
        if format_id is None and not best:
            format_id = next((f['format_id'] for f in info['formats'] if 'mp4' in f['ext']), None)
        if format_id:
            ydl_opts['format'] = format_id
        elif best:
            ydl_opts['format'] = 'bestvideo+bestaudio/best'

        result = io.BytesIO()
        ydl_opts['outtmpl'] = result

        # Use yt-dlp to download directly to the BytesIO object
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        result.seek(0)
        return result, info['title'] + '.mp4'


def stream_video_from_url(video_url, title):
    # Make a request to the video URL to get the stream
    r = requests.get(video_url, stream=True)

    safe_title = quote(f"{title}.mp4")

    # If the response status is OK, proceed to stream
    if r.status_code == 200:
        # Set up a response with dynamic content disposition
        headers = {
            'Content-Disposition': f"attachment; filename*=UTF-8''{safe_title}",  # Dynamic title
            'Content-Type': r.headers.get('Content-Type', 'application/octet-stream')
        }

        # Stream the content with headers
        return Response(r.iter_content(chunk_size=1024), headers=headers)
    else:
        # If video URL is not accessible, return an error
        return "Unable to stream video", 50


@app.route('/download')
def download():
    url = request.args.get('url')
    title = request.args.get('title')
    audio_url = request.args.get('audio')
    platform = request.args.get('platform')

    if not url:
        return 'URL is required.', 400

    if platform == 'instagram' or platform == 'youtube':
        # Merge the video and audio
        merged_video = merge_video_audio(url, audio_url)

        # Serve the merged video to the client
        return send_file(merged_video, mimetype='video/mp4', as_attachment=True, download_name=f'{title}.mp4')

    return stream_video_from_url(url, title)


@app.route('/download_best')
def download_best():
    url = request.args.get('url')
    title = request.args.get('title')
    audio_url = request.args.get('audio')
    platform = request.args.get('platform')

    if not url:
        return 'URL is required.', 400

    if platform == 'instagram':
        # Merge the video and audio
        merged_video = merge_video_audio(url, audio_url)

        # Serve the merged video to the client
        return send_file(merged_video, mimetype='video/mp4', as_attachment=True, download_name=f'{title}.mp4')

    return stream_video_from_url(url, title)


if __name__ == '__main__':
    app.run(debug=True)
