#!/bin/sh
echo "Initializing localstack s3"

echo "Creating bucket"
aws s3 mb s3://clone-ingestion-messages --endpoint-url http://localhost:4566

echo "Uploading resources"
aws s3 cp ./2023-03-30.json s3://clone-ingestion-messages/uuid-val/slack/2023-03-30.json --endpoint-url http://localhost:4566
