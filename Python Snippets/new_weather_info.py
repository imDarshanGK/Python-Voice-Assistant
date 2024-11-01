import requests
import json
import logging

API_KEY = 'YOUR_API_KEY' #Replace with your OpenWeatherMap API key
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"
FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast?"
ONE_CALL_URL = "http://api.openweathermap.org/data/2.5/onecall?"
FAVOURITE_CITIES_FILE = "favourite_cities.json"

logging.basicConfig(filename="weather_info.log", level=logging.INFO, 
                    format="%(asctime)s - %(levelname)s - %(message)s")

def log_api_call(city_name, response):
    if response.status_code == 200:
        logging.info(f"Successfully fetched weather for {city_name}")
    else:
        logging.error(f"Failed to fetch weather for {city_name}: {response.status_code} {response.text}")

def get_weather(city_name, unit="metric"):
    try:
        unit_param = {"metric": "°C", "imperial": "°F", "kelvin": "K"}
        complete_url = BASE_URL + f"q={city_name}&units={unit}&appid=" + API_KEY
        response = requests.get(complete_url)
        log_api_call(city_name, response)

        data = response.json()
        if response.status_code != 200:
            return f"Error: {data.get('message', 'Unable to retrieve weather data.')}"

        if data["cod"] == "404":
            return "City not found. Please check the city name."

        main = data["main"]
        weather_description = data["weather"][0]["description"]
        temperature = main["temp"]
        weather_info = f"Temperature: {temperature:.2f}{unit_param[unit]}\nDescription: {weather_description}"
        
        return weather_info
    except requests.exceptions.RequestException as e:
        logging.error(f"Request failed: {str(e)}")
        return f"Error: Unable to fetch data. {str(e)}"

def get_weather_forecast(city_name):
   
    complete_url = FORECAST_URL + "q=" + city_name + "&appid=" + API_KEY + "&units=metric"
    response = requests.get(complete_url)
    data = response.json()
    
    if data["cod"] != "404":
        forecast_list = data["list"]
        forecast_info = []
        for forecast in forecast_list[::8]:  
            date = forecast["dt_txt"].split(" ")[0]  
            temperature = forecast["main"]["temp"]  
            description = forecast["weather"][0]["description"]
            forecast_info.append(f"{date} - Temperature: {temperature:.2f}°C, Description: {description}")
        return "\n".join(forecast_info)
    else:
        return "City not found"

def get_weather_alerts(lat, lon):
    complete_url = ONE_CALL_URL + f"lat={lat}&lon={lon}&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()
    
    if "alerts" in data:
        alerts = data["alerts"]
        alert_info = []
        for alert in alerts:
            event = alert["event"]
            description = alert["description"]
            start = alert["start"]
            end = alert["end"]
            alert_info.append(f"Alert: {event}\nDescription: {description}\nStart: {start}\nEnd: {end}")
        return "\n".join(alert_info)
    else:
        return "No weather alerts"

def save_favourite_city(city_name):
    try:
        with open(FAVOURITE_CITIES_FILE, 'r+') as file:
            cities = json.load(file)
            if city_name not in cities:
                cities.append(city_name)
                file.seek(0)
                json.dump(cities, file)
        return "City added to favourites"
    except FileNotFoundError:
        with open(FAVOURITE_CITIES_FILE, 'w') as file:
            json.dump([city_name], file)
        return "Favourites file created and city added"

def get_favourite_cities():
    try:
        with open(FAVOURITE_CITIES_FILE, 'r') as file:
            cities = json.load(file)
        return cities
    except FileNotFoundError:
        return "No favourite cities saved"
