import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_all_recommendations(music, books, movies, cuisines, dietary, hobbies):
    prompt = f"""
    User's preferences:
    - Music genres: {music}
    - Book genres: {books}
    - Movie genres: {movies}
    - Cuisines: {cuisines}
    - Dietary requirements: {dietary}
    - Hobbies: {hobbies}

    Based on the user's preferences, suggest a minimum of 10 recommendations for each category.
    TAKE CAUTION THAT THE RECIPES YOU SUGGEST MEET THE DIETARY REQUIREMENTS.
    Respond with ONLY a valid JSON object, no extra description, no extra text:
    {{
        "music": ["Artist - Song", ...],
        "books": ["Author - Title", ...],
        "movies": ["Title (Year)", ...],
        "recipes": ["Meal Name", ...],
        "activities": ["Activity", ...]
    }}
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("registration.html")

@app.route("/quiz")
def quiz():
    return render_template("quizUI.html")

@app.route("/dashboard")
def dashboard():
    return render_template("base.html")

@app.route("/save-preferences", methods=["POST"])
def save_preferences():
    data = request.get_json()

    music    = data.get("music", [])
    books    = data.get("books", [])
    movies   = data.get("movies", [])
    cuisines = data.get("cuisines", [])
    dietary  = data.get("dietary", [])
    hobbies  = data.get("hobbies", [])

    recommendations = recommendations = get_all_recommendations(music, books, movies, cuisines, dietary, hobbies)

    return jsonify({"status": "ok", "recommendations": recommendations})

if __name__ == "__main__":
    app.run(debug=True)