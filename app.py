from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

YOUTUBE_API_KEY = "add your api"

def get_youtube_videos(query):
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        'part': 'snippet',
        'q': query,
        'type': 'video',
        'maxResults': 5,
        'key': YOUTUBE_API_KEY
    }
    res = requests.get(url, params=params).json()

    videos = []
    for item in res.get("items", []):
        title = item["snippet"]["title"]
        video_id = item["id"]["videoId"]
        thumbnail = item["snippet"]["thumbnails"]["high"]["url"]
        videos.append({
            "title": title,
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": thumbnail
        })
    return videos

@app.route("/suggest", methods=["POST"])
def suggest():
    data = request.get_json()
    query = data.get("query")
    suggestions = get_youtube_videos(query)
    return jsonify({"suggestions": suggestions})

if __name__ == "__main__":
    app.run(debug=True)
