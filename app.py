import streamlit as st
import requests

# 1. Title and Description
st.title("🌤️ Simple AI Weather Agent by Shivadeep102")
st.write("Enter any city below to get real-time weather using Open-Meteo's free API.")

# 2. User Input
city = st.text_input("Enter Location (e.g., Tokyo, Paris, New York):", placeholder="Brentwood, CA")

# 3. Agent Logic Function
def weather_agent(location_name):
    if not location_name.strip():
        return "Please enter a valid city name."
    
    clean_location = location_name.strip()
    
    # 🔗 FIX 1: Use the correct Geocoding API domain, path, and '?name=' query structure
    geo_url = "https://open-meteo.com"
    geo_params = {
        "name": clean_location,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        # Using the 'params' argument automatically structures the URL safely
        geo_res = requests.get(geo_url, params=geo_params).json()
        if "results" not in geo_res or not geo_res["results"]:
            return f"❌ Could not find a location named '{clean_location}'."
        
        loc_data = geo_res["results"][0]
        lat = loc_data["latitude"]
        lon = loc_data["longitude"]
        full_name = f"{loc_data['name']}, {loc_data.get('country', '')}"
        
        # 🔗 FIX 2: Use the correct Forecast API domain, path, and parameters
        weather_url = "https://open-meteo.com"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature"
        }
        
        weather_res = requests.get(weather_url, params=weather_params).json()
        
        current = weather_res["current"]
        return {
            "location": full_name,
            "temp": current["temperature_2m"],
            "feels_like": current["apparent_temperature"],
            "humidity": current["relative_humidity_2m"]
        }
    except Exception as e:
        return f"⚠️ Error processing your request: {str(e)}"

# 4. Trigger & Output Display
if st.button("Ask Agent"):
    with st.spinner("Agent is analyzing location and fetching live data..."):
        result = weather_agent(city)
        
        if isinstance(result, dict):
            st.success(f"### Weather for {result['location']}")
            col1, col2, col3 = st.columns(3)
            col1.metric("Temperature", f"{result['temp']}°C")
            col2.metric("Feels Like", f"{result['feels_like']}°C")
            col3.metric("Humidity", f"{result['humidity']}%")
        else:
            st.error(result)
