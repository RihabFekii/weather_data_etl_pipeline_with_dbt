import pytest
from unittest.mock import patch, MagicMock
from src.data_collection import fetch_weather_data
from src.data_transformation import transform_data 
from src.utils import export_to_cloud_storage

# --- Fixtures ---

@pytest.fixture
def mock_get_storage_client():
    """Mocks the get_storage_client function."""
    with patch("src.utils.get_storage_client") as mock:
        mock_storage_client = MagicMock()
        mock.return_value = mock_storage_client  # Return a mock storage client
        yield mock

@pytest.fixture
def mock_fetch_weather_data():
    with patch("src.data_collection.requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.json.return_value = {'name': 'Tunis', 'main': {'temp': 20}}
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        yield mock_get

@pytest.fixture
def mock_transform_data():
    """Mocks the transform_data function."""
    with patch("src.data_transformation.transform_data") as mock:
        mock.return_value = {'city': 'Tunis', 'temperature': 20}  # Mock the transformed data structure
        yield mock

@pytest.fixture
def mock_config():
    """Mocks the configuration settings."""
    return {"bucket_name": "test-bucket"}

# --- Tests ---

def test_fetch_weather_data(mock_fetch_weather_data):
    """Tests the fetch_weather_data function."""
    result = fetch_weather_data('Tunis')
    assert result == {'name': 'Tunis', 'main': {'temp': 20}}
    mock_fetch_weather_data.assert_called_once()

def test_transform_data():
    """Tests the transform_data function."""
    input_data = {
        'name': 'Tunis',
        'main': {'temp': 20, 'humidity': 50, 'pressure': 1013},
        'wind': {'speed': 5},
        'weather': [{'description': 'Clear sky'}]
    }
    result = transform_data(input_data)
    assert result['city'] == 'Tunis'
    assert result['temperature'] == 20

def test_export_to_cloud_storage(mock_get_storage_client, mock_config):
    """Tests the export_to_cloud_storage function."""
    # Arrange
    mock_storage_client = mock_get_storage_client.return_value
    mock_bucket = MagicMock()
    mock_blob = MagicMock()
    mock_storage_client.bucket.return_value = mock_bucket
    mock_bucket.blob.return_value = mock_blob

    data = [{'city': 'Tunis', 'temperature': 20}]
    bucket_name = mock_config["bucket_name"]
    blob_name = "test-blob"

    # Act
    export_to_cloud_storage(data, bucket_name, blob_name)

    # Assert
    mock_get_storage_client.assert_called_once()
    mock_storage_client.bucket.assert_called_once_with(bucket_name)
    mock_bucket.blob.assert_called_once_with(blob_name + ".csv")  # Check for ".csv"
    mock_blob.upload_from_string.assert_called_once()

