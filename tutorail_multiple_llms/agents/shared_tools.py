def get_weather(city: str) -> dict:
    city_normalized = city.lower().replace(" ", "")
    mock_weather_db = {
        "newyork": {"status": "success", "report": "Sunny in New York, 25°C"},
        "london": {"status": "success", "report": "Cloudy in London, 15°C"},
        "tokyo": {"status": "success", "report": "Rainy in Tokyo, 18°C"},
    }
    return mock_weather_db.get(city_normalized, {
        "status": "error",
        "error_message": f"Sorry, I don't have weather info for {city}."
    })
