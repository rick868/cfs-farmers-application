import random
from  datetime import date

def get_weather_data(location="Nairobi"):
    """
    Simulates fetching weather data from an API.
    """
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy"]
    temp = random.randint(18, 30)
    condition = random.choice(conditions)
    rain_chance = random.randint(0, 80) if condition in ["Rainy", "Cloudy"] else random.randint(0, 20)
    
    return {
        "location": location,
        "temperature": temp,
        "condition": condition,
        "rain_chance": rain_chance,
        "date": date.today().strftime("%A, %d %B")
    }

def get_market_prices():
    """
    Returns mock market prices for common crops.
    """
    return [
        {"crop": "Maize (90kg)", "price": 4500, "change": "+5%"},
        {"crop": "Beans (90kg)", "price": 8200, "change": "-2%"},
        {"crop": "Potatoes (50kg)", "price": 2500, "change": "+1.5%"},
        {"crop": "Coffee (kg)", "price": 85, "change": "+0.5%"},
        {"crop": "Tea (kg)", "price": 60, "change": "0%"},
    ]

def get_farming_tips():
    """
    Returns a random farming tip.
    """
    tips = [
        "Rotate crops to maintain soil fertility and reduce pests.",
        "Test your soil pH before applying fertilizers.",
        "Mulching helps retain soil moisture during dry spells.",
        "Scout for fall armyworm early in the morning.",
        "Use certified seeds for better germination rates."
    ]
    return random.choice(tips)

def get_officer_stats():
    """
    Returns mock stats for the extension officer dashboard.
    """
    return {
        "assigned_farmers": 45,
        "pending_visits": 3,
        "alerts_active": 1,
        "region": "Rift Valley"
    }
