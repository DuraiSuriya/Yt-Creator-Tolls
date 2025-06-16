from flask import Flask, request, send_file, jsonify
from yt_dlp import YoutubeDL
import uuid
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "YouTube Downloader API is running!"

@app.route("/download", methods=["POST"])
def download():
    data = request.get_json()
    video_url = data.get("url")

    if not video_url:
        return jsonify({"error": "No URL provided"}), 400

    # Unique filename
    filename = f"video_{uuid.uuid4()}.mp4"

    # yt-dlp options
    ydl_opts = {
        "outtmpl": filename,
        "format": "best[ext=mp4]",
        "quiet": True,
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # Send file as response
    response = send_file(filename, as_attachment=True)

    # Remove file after sending
    os.remove(filename)
    return response

if __name__ == "__main__":
    app.run(debug=True)
