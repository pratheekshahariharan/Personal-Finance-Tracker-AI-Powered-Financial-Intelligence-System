import os
from google import genai
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("GEMINI_API_KEY")

print(f"Key found: {bool(key)}")
if key:
    print(f"Key starts with: {key[:10]}...")

try:
    client = genai.Client(api_key=key)
    response = client.models.generate_content(
        model='gemini-2.0-flash-exp',
        contents="Hello, this is a diagnostic test. Please reply with 'READY'."
    )
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
