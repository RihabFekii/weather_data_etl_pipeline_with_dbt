# weather_data_etl_pipeline_with_dbt
Building a Weather Data ETL Pipeline with OpenWeatherMap API, dbt &amp; GCP



## Deploying the ETL pipeline

After creating a docker image of the python service to fetch data from weather data API. 
The next step is to build and push the Docker image to Google Container Registry:

```bash
docker build -t gcr.io/your-project-id/weather-etl:v1 .
docker push gcr.io/your-project-id/weather-etl:v1
````

Then, deploy to Cloud Run: 

```bash
gcloud run deploy weather-etl --image gcr.io/your-project-id/weather-etl:v1 \
  --platform managed \
  --region us-central1 \
  --set-env-vars OPENWEATHERMAP_API_KEY=your-api-key
````

Set up Cloud Scheduler to run the service hourly:

```bash
gcloud scheduler jobs create http weather-etl-job \
  --schedule "0 * * * *" \
  --uri "https://your-cloud-run-service-url" \
  --http-method POST
```


