#!/bin/sh
echo "Initializing localstack s3"

awslocal s3 mb s3://clone-ingestion-messages --endpoint-url http://localhost:4566
awslocal s3 cp /etc/localstack/init/ready.d/2023-03-30.json s3://clone-ingestion-messages/uuid-val/slack/2023-03-30.json --endpoint-url http://localhost:4566