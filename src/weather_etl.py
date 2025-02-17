import json
import logging
from google.cloud import storage
from datetime import datetime

from data_collection import fetch_weather_data
from data_transformation import transform_data
from utils import export_to_cloud_storage


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)


CITIES = config['cities']

def main():
    logger.info("Starting weather data collection and export process")
    all_data = []
    for city in CITIES:
        logger.debug(f"Fetching weather data for {city}")
        raw_data = fetch_weather_data(city)
        if raw_data:
            transformed_data = transform_data(raw_data)
            if transformed_data:
                all_data.append(transformed_data)

    if all_data:
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        export_to_cloud_storage(all_data, config['bucket_name'], f"weather_data_{timestamp}")  # Changed the extension to .csv in export
        logger.info("Weather data collection and export process completed")
    else:
        logger.warning("No data to export")


if __name__ == "__main__":
    main()
