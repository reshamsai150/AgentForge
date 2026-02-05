import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

models = [
    'gemini-1.5-flash',
    'gemini-1.5-flash-latest',
    'gemini-1.5-pro',
    'gemini-pro',
    'gemini-1.0-pro'
]

print("Testing Gemini Models...")
for m_name in models:
    try:
        model = genai.GenerativeModel(m_name)
        response = model.generate_content('hi')
        print(f"SUCCESS: {m_name}")
        # Stop at the first working one
        break
    except Exception as e:
        print(f"FAILED {m_name}: {str(e)}")
