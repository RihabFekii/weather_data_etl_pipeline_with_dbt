import json
import logging
from google.cloud import storage
from datetime import datetime


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load configuration
with open('config/config.json', 'r') as config_file:
    config = json.load(config_file)

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
