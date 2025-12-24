import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load env variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ FINAL, WORKING MODEL
model = genai.GenerativeModel("models/gemini-flash-latest")


def ask_gemini(prompt: str) -> str:
    """
    Send prompt to Gemini and return text response
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error from Gemini: {str(e)}"
