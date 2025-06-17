#!/bin/bash

# Deploy Backend
cd backend
echo "Building backend..."
gcloud builds submit . --tag gcr.io/proven-airship-284111/k2-spiral-backend

echo "Deploying backend..."
gcloud run deploy k2-spiral-backend \
  --image gcr.io/proven-airship-284111/k2-spiral-backend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --timeout 300s \
  --memory 512Mi

# Get backend URL dynamically
BACKEND_SERVICE_URL=$(gcloud run services describe k2-spiral-backend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')
echo "Backend service URL: $BACKEND_SERVICE_URL"

# Deploy Frontend using Cloud Build with config
cd ../frontend
echo "Building frontend..."
# Create a temporary cloudbuild.yaml file
cat > cloudbuild.yaml << EOF
steps:
- name: 'gcr.io/cloud-builders/docker'
  args: ['build', 
         '--build-arg', 'REACT_APP_API_URL=${BACKEND_SERVICE_URL}',
         '-t', 'gcr.io/proven-airship-284111/k2-spiral-frontend', '.']
images:
- 'gcr.io/proven-airship-284111/k2-spiral-frontend'
EOF

# Use Cloud Build with the config file
gcloud builds submit --config=cloudbuild.yaml

echo "Deploying frontend..."
gcloud run deploy k2-spiral-frontend \
  --image gcr.io/proven-airship-284111/k2-spiral-frontend \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated

# Get frontend URL
FRONTEND_URL=$(gcloud run services describe k2-spiral-frontend \
  --platform managed \
  --region us-central1 \
  --format 'value(status.url)')
echo "Frontend deployed at: $FRONTEND_URL"

echo "Deployment complete!"