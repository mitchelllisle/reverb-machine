PROJECT_ID=reverb-machine
REGION=australia-southeast1
TIMEOUT=540s
TOPIC=reverb-pedals
FUNCTION_NAME=SaveReverbListingsToGCS

echo "Deploying $FUNCTION_NAME to project $PROJECT_ID"

gcloud functions deploy $FUNCTION_NAME \
  --project=$PROJECT_ID \
  --region=$REGION \
  --set-env-vars GOOGLE_PROJECT_ID=$PROJECT_ID \
  --runtime python37 \
  --timeout $TIMEOUT \
  --trigger-topic $TOPIC
