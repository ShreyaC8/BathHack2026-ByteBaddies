import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_music_recommendations(selected_music: list) -> list:
    prompt = f"""
    The user enjoys these music genres: {selected_music}.
    Suggest a minimum of 10 music recommendations based on the user's music genre preferences.
    Respond with ONLY a valid JSON array of strings, no descriptions, no extra text.
    Example format: ["Artist - Song", "Artist - Song", "Artist - Song"]
    """
    
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

def get_book_recommendations(selected_books: list) -> list:
    prompt = f"""
    The user enjoys these book genres: {selected_books}.
    Suggest a minimum of 10 book recommendations based on the user's book genre preferences.
    Respond with ONLY a valid JSON array of strings, no descriptions, no extra text.
    Example format: ["Author - Title", "Author - Title", "Author - Title"]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)


def get_movie_recommendations(selected_movies: list) -> list:
    prompt = f"""
    The user enjoys these movie genres: {selected_movies}.
    Suggest a minimum of 10 movie recommendations based on the user's movie genre preferences.
    Respond with ONLY a valid JSON array of strings, no descriptions, no extra text.
    Example format: ["Title (Year)", "Title (Year)", "Title (Year)"]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

def get_recipe_recommendations(selected_dietry_requirements: list, selected_cuisines: list) -> list:
    prompt = f"""
    The user has these following strict dietary requirements: {selected_dietry_requirements}.
    The user enjoys these following cuisines: {selected_cuisines}.
    Suggest a minimum of 10 recipe recommendations based on the user's dietary requirements and preferred cuisines.
    Respond with ONLY a valid JSON array of strings, no extra descriptions, no extra text.
    Example format: ["Name of Meal - Recipe", "Name of Meal - Recipe", "Name of Meal - Recipe"]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

def get_activity_recommendations(selected_hobbies: list) -> list:
    prompt = f"""
    The user enjoys these following hobbies: {selected_hobbies}.
    Suggest a minimum of 10 activity recommendations based on the user's hobby preferences.
    Respond with ONLY a valid JSON array of strings, no descriptions, no extra text.
    Example format: ["Hobby", "Hobby", "Hobby"]
    """
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )
    raw = response.text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    return json.loads(raw)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("quizUI.html")

@app.route("/save-preferences", methods=["POST"])
def save_preferences():
    data = request.get_json()

    music    = data.get("music", [])
    books    = data.get("books", [])
    movies   = data.get("movies", [])
    cuisines = data.get("cuisines", [])
    dietary  = data.get("dietary", [])
    hobbies  = data.get("hobbies", [])

    recommendations = {
        "music":      get_music_recommendations(music),
        "books":      get_book_recommendations(books),
        "movies":     get_movie_recommendations(movies),
        "recipes":    get_recipe_recommendations(dietary, cuisines),
        "activities": get_activity_recommendations(hobbies)
    }    

    print(recommendations)

    return jsonify({"status": "ok", "recommendations": recommendations})


if __name__ == "__main__":
    app.run(debug=True)