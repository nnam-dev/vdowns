import requests


def download_tiktok_video_direct(video_url):
    try:
        # Send a GET request to the video URL
        response = requests.get(video_url, stream=True)

        # Check if the response status is 200 (OK)
        if response.status_code == 200:
            video_filename = 'tiktok_video.mp4'

            # Write the video content to a file
            with open(video_filename, 'wb') as video_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        video_file.write(chunk)

            print(f"Video downloaded successfully as {video_filename}!")
        else:
            print(f"Failed to download the video. Status code: {response.status_code}")

    except Exception as e:
        print(f"An error occurred: {e}")


# Example TikTok video URL (you need to provide a direct URL)
video_url = "https://www.tiktok.com/@iamdikeh/video/7413283334639324421?is_from_webapp=1"
download_tiktok_video_direct(video_url)
