import pytest
from unittest.mock import patch, MagicMock
from src.weather_etl import fetch_weather_data, transform_data, export_to_cloud_storage

@patch('weather_etl.requests.get')
def test_fetch_weather_data(mock_get):
    mock_response = MagicMock()
    mock_response.json.return_value = {'name': 'Test City', 'main': {'temp': 20}}
    mock_get.return_value = mock_response

    result = fetch_weather_data('Test City')
    assert result['name'] == 'Test City'

def test_transform_data():
    input_data = {
        'name': 'Test City',
        'main': {'temp': 20, 'humidity': 50, 'pressure': 1013},
        'wind': {'speed': 5},
        'weather': [{'description': 'Clear sky'}]
    }
    result = transform_data(input_data)
    assert result['city'] == 'Test City'
    assert result['temperature'] == 20

@patch('weather_etl.storage.Client')
def test_export_to_cloud_storage(mock_client):
    mock_bucket = MagicMock()
    mock_client.return_value.bucket.return_value = mock_bucket

    export_to_cloud_storage({'test': 'data'}, 'test-bucket', 'test-blob')
    mock_bucket.blob.assert_called_once_with('test-blob')
    mock_bucket.blob.return_value.upload_from_string.assert_called_once()
