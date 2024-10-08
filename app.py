from flask import Flask, request, send_file, jsonify, render_template
import os
import tempfile
import yt_dlp

app = Flask(__name__)

# Temporary directory for storing downloads
TEMP_DIR = tempfile.gettempdir()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download_video():
    url = request.json.get('url')
    cookies = request.json.get('cookies')  # Expect cookies to be passed in JSON format
    
    if not url:
        return jsonify({"error": "URL is required"}), 400

    # Set up options for yt-dlp
    ydl_opts = {
        'cookiefile': None,
        'outtmpl': os.path.join(TEMP_DIR, '%(title)s.%(ext)s'),
        'format': 'best'
    }

    # If cookies are provided, write them to a temporary cookie file
    if cookies:
        cookie_file_path = os.path.join(TEMP_DIR, 'cookies.txt')
        with open(cookie_file_path, 'w') as f:
            f.write(cookies)
        ydl_opts['cookiefile'] = cookie_file_path

    # Download the video
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info_dict)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Provide the download link
    return jsonify({"download_link": f"/download_file?filename={os.path.basename(file_path)}"}), 200

@app.route('/download_file', methods=['GET'])
def download_file():
    filename = request.args.get('filename')
    file_path = os.path.join(TEMP_DIR, filename)

    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return jsonify({"error": "File not found"}), 404

@app.route('/delete_file', methods=['DELETE'])
def delete_file():
    filename = request.args.get('filename')
    file_path = os.path.join(TEMP_DIR, filename)

    if os.path.isfile(file_path):
        os.remove(file_path)
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "File not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
