from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

CLIENT_ID = "15e2ce55d5e94dbb8bd11133b6b997c6"
CLIENT_SECRET = "7465ffc4c2e443648164b43b2bcada8d"

app = Flask(__name__) 
CORS(app)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Get Spotify Token
def get_spotify_token():
    url = "https://accounts.spotify.com/api/token"
    data = {"grant_type": "client_credentials"}
    auth = (CLIENT_ID, CLIENT_SECRET)
    response = requests.post(url, data=data, auth=auth)
    return response.json().get("access_token")

ACCESS_TOKEN = get_spotify_token()

# Capsule Model
class Capsule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    songs = db.Column(db.String(500))  # Store Spotify URLs as a comma-separated string
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"Time Capsule('{self.title}', '{self.created_at}')"

# Initialize Database
with app.app_context():
    db.create_all()

@app.route("/")
def home():
    return "Time Capsule API is running!"

@app.route("/create_capsule", methods=["POST"])
def create_capsule():
    data = request.json
    title = data.get("title")
    description = data.get("description", "")
    songs = data.get("songs", "")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    new_capsule = Capsule(title=title, description=description, songs=songs)
    db.session.add(new_capsule)
    db.session.commit()

    return jsonify({
        "message": "Capsule created successfully",
        "capsule_id": new_capsule.id
    })

@app.route('/search', methods=["GET"])
def search_songs(): 
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query parameter"}), 400
    
    url = f"https://api.spotify.com/v1/search?q={query}&type=track&limit=5"
    headers = {"Authorization": f"Bearer {ACCESS_TOKEN}"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return jsonify({"error": "Failed to fetch songs"}), response.status_code

    songs = response.json()["tracks"]["items"]
    results = [
        {
            "song_name": song["name"],
            "artist": song["artists"][0]["name"],
            "album_art": song["album"]["images"][0]["url"],
            "spotify_url": song["external_urls"]["spotify"]
        }
        for song in songs
    ]
    return jsonify(results)

if __name__ == "__main__": 
    app.run(debug=True)
