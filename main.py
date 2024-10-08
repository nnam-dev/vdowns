import subprocess

# Define the URL of the video you want to download
video_url = "https://youtube.com/shorts/2ON2kzUnoxA?si=0LfjdoQB7vu17rPl"  # Replace with the actual video URL

# Construct the yt-dlp command with the option to use cookies from Chrome
command = [
    "yt-dlp",
    "--cookies-from-browser", "chrome",  # Use Chrome cookies
    video_url
]

try:
    # Run the yt-dlp command
    result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    # Print the output
    print(result.stdout.decode())
except subprocess.CalledProcessError as e:
    # Handle errors
    print("Error occurred while downloading the video:")
    print(e.stderr.decode())
