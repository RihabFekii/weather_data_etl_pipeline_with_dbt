FROM python:3.12.2-slim

WORKDIR /app

# Copy the service account key into the container
COPY gcp_credentials.json /app/gcp_credentials.json

# Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
#ARG GOOGLE_APPLICATION_CREDENTIALS
#ENV GOOGLE_APPLICATION_CREDENTIALS=/app/gcp_credentials.json

# Install system dependencies
RUN apt-get update && apt-get install -y curl apt-transport-https ca-certificates

# Install Google Cloud SDK
RUN curl -sSL https://sdk.cloud.google.com | bash
ENV PATH $PATH:/root/google-cloud-sdk/bin

RUN pip install google-cloud-storage

# Authenticate gcloud
RUN gcloud auth activate-service-account --key-file=/app/gcp_credentials.json

# Configure docker to use gcloud
RUN gcloud auth configure-docker

# Install pip packages with authentication support
RUN pip install --upgrade pip && \
    pip install --no-cache-dir keyrings.google-artifactregistry-auth && \
    pip install --no-cache-dir weather-data-etl==0.1.0 --extra-index-url https://europe-west10-python.pkg.dev/dd-testtask-rf-016d/weather-data-etl/simple/

# Copy the source code
COPY src/ /app/src/
COPY config/config.json /app/config/config.json


COPY requirements.txt .
RUN pip install -r requirements.txt

CMD ["python", "/app/src/weather_etl.py"]
