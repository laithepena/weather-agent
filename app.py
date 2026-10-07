import streamlit as st
import requests

# 1. Title and Description
st.title("🌤️ Simple AI Weather Agent by Shivadeep11")
st.write("Enter any city below to get real-time weather using Open-Meteo's free API.")

# 2. User Input
city = st.text_input("Enter Location (e.g., Tokyo, Paris, New York):", placeholder="Brentwood, CA")

# 3. Agent Logic Function
def weather_agent(location_name):
    if not location_name.strip():
        return "Please enter a valid city name."
    
    # ✅ FIX: Properly formatted API URL
    geo_url = f"https://open-meteo.com{location_name}&count=1&language=en&format=json"
    
    try:
        geo_res = requests.get(geo_url).json()
        if "results" not in geo_res or not geo_res["results"]:
            return f"❌ Could not find a location named '{location_name}'."
        
        # Grab the first match
        loc_data = geo_res["results"][0]
        lat, lon = loc_data["latitude"], loc_data["longitude"]
        full_name = f"{loc_data['name']}, {loc_data.get('country', '')}"
        
        # Step 2: Fetch weather details
        weather_url = f"https://open-meteo.com{lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code"
        weather_res = requests.get(weather_url).json()
        
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
