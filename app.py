import streamlit as st
import requests

# 1. Title and Description
st.title("🌤️ AI Weather Agent by Rudee Pudee")
st.write("Enter any city below to get real-time weather using Open-Meteo's free API.")

# 2. User Input
city = st.text_input("Enter Location (e.g., Tokyo, Paris, New York):", placeholder="Brentwood, CA")

# 3. Agent Logic Function
def weather_agent(location_name):
    if not location_name.strip():
        return "Please enter a valid city name."
    
    clean_location = location_name.strip()
    
    # --- STEP 1: Fetch Geocoding Coordinates ---
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": clean_location,
        "count": 1,
        "language": "en",
        "format": "json"
    }
    
    try:
        geo_response = requests.get(geo_url, params=geo_params)
        geo_response.raise_for_status() 
        geo_res = geo_response.json()
        
        # Verify the key exists and has items
        if "results" not in geo_res or not geo_res["results"]:
            return f"❌ Could not find a location named '{clean_location}'."
        
        # Extract the first dictionary item inside the list array using [0]
        loc_data = geo_res["results"][0]
        
        lat = loc_data["latitude"]
        lon = loc_data["longitude"]
        full_name = f"{loc_data['name']}, {loc_data.get('country', '')}"
        
        # --- STEP 2: Fetch Live Weather ---
        weather_url = "https://api.open-meteo.com/v1/forecast"
        weather_params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature",
            "temperature_unit": "fahrenheit",  # Server returns numbers in Fahrenheit
            "timezone": "auto"
        }
        
        weather_response = requests.get(weather_url, params=weather_params)
        weather_response.raise_for_status() 
        weather_res = weather_response.json()
        
        if "current" not in weather_res:
            return "❌ Weather data format returned from the server was unexpected."
            
        current = weather_res["current"]
        return {
            "location": full_name,
            "temp": current.get("temperature_2m", "N/A"),
            "feels_like": current.get("apparent_temperature", "N/A"),
            "humidity": current.get("relative_humidity_2m", "N/A")
        }
        
    except requests.exceptions.HTTPError as http_err:
        return f"⚠️ API Server Error occurred: {http_err}"
    except Exception as e:
        return f"⚠️ Error processing your request: {str(e)}"


# 4. Trigger & Output Display
if st.button("Ask Agent Rudee"):
    with st.spinner("Agent is analyzing location and fetching live data..."):
        result = weather_agent(city)
        
        if isinstance(result, dict):
            st.success(f"### Weather for {result['location']}")
            col1, col2, col3 = st.columns(3)
            # ✅ FIXED: Display labels updated to show °F instead of °C
            col1.metric("Temperature", f"{result['temp']}°F")
            col2.metric("Feels Like", f"{result['feels_like']}°F")
            col3.metric("Humidity", f"{result['humidity']}%")
        else:
            st.error(result)
