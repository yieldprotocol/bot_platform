#!/bin/bash

# bash variable to set gcr.io/chatweb3-380221/bot-platform:latest
image_tag=gcr.io/chatweb3-380221/bot-platform:latest

docker build -t $image_tag .

docker push $image_tag

old_revision=$(gcloud run revisions list --platform managed --region us-east1 --service bot-platform-dev --format="value(metadata.name)")

gcloud run deploy bot-platform-dev --image $image_tag

gcloud run revisions delete $old_revision --platform managed --region us-east1  --quiet