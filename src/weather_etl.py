import requests
import json
import logging
from google.cloud import storage
from datetime import datetime
import os

from src.data_collection import fetch_weather_data
from src.data_transformation import transform_data, export_to_cloud_storage


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
CITIES = config['cities']
COLUMNS_TO_IGNORE = config['columns_to_ignore']


def main():
    all_data = []
    for city in CITIES:
        raw_data = fetch_weather_data(city)
        if raw_data:
            transformed_data = transform_data(raw_data)
            if transformed_data:
                all_data.append(transformed_data)
    
    if all_data:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        export_to_cloud_storage(all_data, config['bucket_name'], f"weather_data_{timestamp}.json")
    else:
        logger.warning("No data to export")

if __name__ == "__main__":
    main()