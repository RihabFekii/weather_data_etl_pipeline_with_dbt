# weather_data_etl_pipeline_with_dbt
Building a Weather Data ETL Pipeline with OpenWeatherMap API, dbt &amp; BigQuery.

## 📖 Project overview
This project consists of the following tasks: 
1. Implmenting an ETL with Python that retrievs Weather data from the open WeatherMap API. 
2. Deploying the Python service with Docker in Cloud Run on GCP.
3. Developping an data analysis & modeling sevrice with dbt.

## 🏗️ Architecture

The following is the highlevel architecture of the project: 

![Data Architecture](/docs/Data%20Architecture.png)

## Deploying the ETL pipeline

The Python Package was containerized with Docker and the Docker image was pushed to the GCP Artifact Registry. 

To pull the image, run the following instruction: 

`````shell
docker run -p 8080:8080 --env-file .env -e PORT=8080 weather-data-etl-docker-image
`````





