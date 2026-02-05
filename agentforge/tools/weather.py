import httpx
import os
from typing import Dict, Any

def get_weather(location: str) -> Dict[str, Any]:
    """
    Fetch current weather for a location using OpenWeatherMap API.
    Returns a dictionary of results.
    """
    api_key = os.getenv("WEATHER_API_KEY")
    if not api_key:
        return {"error": "Weather API key not found in environment"}
    
    url = f"https://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    
    try:
        response = httpx.get(url, timeout=10.0)
        response.raise_for_status()
        data = response.json()
        
        return {
            "location": data.get("name"),
            "temperature": data.get("main", {}).get("temp"),
            "description": data.get("weather", [{}])[0].get("description"),
            "humidity": data.get("main", {}).get("humidity"),
            "success": True
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
