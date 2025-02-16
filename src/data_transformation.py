import requests
import json
import logging
from google.cloud import storage
from datetime import datetime
import os

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

API_KEY = os.environ.get('OPENWEATHERMAP_API_KEY')
CITIES = config['cities']
COLUMNS_TO_IGNORE = config['columns_to_ignore']

def transform_data(data):
    if not data:
        return None
    
    transformed = {
        'city': data['name'],
        'temperature': data['main']['temp'],
        'humidity': data['main']['humidity'],
        'pressure': data['main']['pressure'],
        'wind_speed': data['wind']['speed'],
        'description': data['weather'][0]['description'],
        'timestamp': datetime.utcnow().isoformat()
    }
    
    return {k: v for k, v in transformed.items() if k not in COLUMNS_TO_IGNORE}

def export_to_cloud_storage(data, bucket_name, blob_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    blob.upload_from_string(json.dumps(data))
    logger.info(f"Data exported to {bucket_name}/{blob_name}")