import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model='gemini-2.5-flash-lite',
    contents="Suggest 3 jazz albums for someone who likes lo-fi hip hop."
)

print(response.text)