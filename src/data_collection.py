import requests
import json
import logging
from google.cloud import storage
from datetime import datetime
import os
from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')
CITIES = config['cities']
COLUMNS_TO_IGNORE = config['columns_to_ignore']


def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"Error fetching data for {city}: {e}")
        return None


fetch_weather_data("London")