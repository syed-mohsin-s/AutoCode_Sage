# AutoCode Sage — Self-Hosted n8n on Google Cloud Run with Cloud SQL

AutoCode Sage is a fully serverless, production-ready setup for running **n8n on Google Cloud Run** using **Cloud SQL (PostgreSQL)** for persistent storage.  
Because Cloud Run containers are stateless and can shut down anytime, Cloud SQL acts as n8n’s long-term memory — ensuring your workflows, credentials, and executions persist.

## Architecture Overview

- **Compute:** Cloud Run (stateless, serverless)
- **Persistent Storage:** Cloud SQL (PostgreSQL)
- **Container Customization:** Custom Docker image with Python (for ML workflows)
- **Port Bridging:** A custom `start.sh` maps Cloud Run’s dynamic `$PORT` to n8n’s fixed port

## Prerequisites

- Google Cloud SDK (`gcloud`) installed and authenticated  
- A Google Cloud Project with billing enabled  
- Basic Docker knowledge

## Deployment Guide

### 1. Initial Setup & Environment Variables

```bash
export PROJECT_ID="your-project-id"
export REGION="us-central1"
export DB_INSTANCE_NAME="n8n-postgres-db"
export DB_NAME="n8n"
export DB_USER="n8nuser"
export DB_PASSWORD="StrongPassword123!"
export REPO_NAME="autocode-sage-repo"
export IMAGE_NAME="n8n-custom"

gcloud auth login
gcloud config set project $PROJECT_ID

gcloud services enable run.googleapis.com \
    sqladmin.googleapis.com \
    artifactregistry.googleapis.com \
    cloudbuild.googleapis.com
```

### 2. Create Cloud SQL Instance

```bash
gcloud sql instances create $DB_INSTANCE_NAME \
    --database-version=POSTGRES_14 \
    --tier=db-f1-micro \
    --region=$REGION \
    --root-password=$DB_PASSWORD

gcloud sql databases create $DB_NAME --instance=$DB_INSTANCE_NAME

gcloud sql users create $DB_USER \
    --instance=$DB_INSTANCE_NAME \
    --password=$DB_PASSWORD
```

### 3. Create Local Config Files

#### start.sh

```bash
#!/bin/sh
export N8N_PORT=$PORT
n8n start
```

#### Dockerfile

```bash
FROM n8nio/n8n:latest

USER root
RUN apk add --no-cache python3 py3-pip
COPY start.sh /start.sh
RUN chmod +x /start.sh
USER node

ENTRYPOINT ["/start.sh"]
```

### 4. Build & Push the Docker Image

```bash
gcloud artifacts repositories create $REPO_NAME \
    --repository-format=docker \
    --location=$REGION \
    --description="Repository for AutoCode Sage n8n"

gcloud builds submit --tag \
    $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest .
```

### 5. Deploy to Cloud Run

```bash
export ENCRYPTION_KEY=$(openssl rand -hex 16)

gcloud run deploy n8n-sage \
    --image $REGION-docker.pkg.dev/$PROJECT_ID/$REPO_NAME/$IMAGE_NAME:latest \
    --region $REGION \
    --platform managed \
    --allow-unauthenticated \
    --min-instances 1 \
    --memory 2Gi \
    --cpu 1 \
    --add-cloudsql-instances $PROJECT_ID:$REGION:$DB_INSTANCE_NAME \
    --set-env-vars "DB_TYPE=postgresdb" \
    --set-env-vars "DB_POSTGRESDB_HOST=/cloudsql/$PROJECT_ID:$REGION:$DB_INSTANCE_NAME" \
    --set-env-vars "DB_POSTGRESDB_USER=$DB_USER" \
    --set-env-vars "DB_POSTGRESDB_PASSWORD=$DB_PASSWORD" \
    --set-env-vars "DB_POSTGRESDB_DATABASE=$DB_NAME" \
    --set-env-vars "N8N_ENCRYPTION_KEY=$ENCRYPTION_KEY"
```

### 6. Set Webhook URLs

```bash
export SERVICE_URL=$(gcloud run services describe n8n-sage \
    --region $REGION \
    --format 'value(status.url)')

gcloud run services update n8n-sage \
    --region $REGION \
    --set-env-vars "WEBHOOK_URL=$SERVICE_URL/" \
    --set-env-vars "WEBHOOK_TUNNEL_URL=$SERVICE_URL/"
```

## Cleanup

```bash
gcloud run services delete n8n-sage --region $REGION
gcloud sql instances delete $DB_INSTANCE_NAME --region $REGION
```
