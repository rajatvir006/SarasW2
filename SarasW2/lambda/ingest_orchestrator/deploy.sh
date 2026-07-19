#!/bin/bash
# deploy.sh — packages and deploys FeedbackIngestOrchestrator, wires the S3 trigger
set -e

BUCKET="ba-feedback-platform-rajatvir"
ACCOUNT_ID="123456789012"

zip function.zip lambda_function.py

aws lambda create-function \
    --function-name FeedbackIngestOrchestrator \
    --runtime python3.12 \
    --role arn:aws:iam::${ACCOUNT_ID}:role/FeedbackLambdaRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://function.zip \
    --timeout 30 --memory-size 256

aws lambda add-permission \
    --function-name FeedbackIngestOrchestrator \
    --statement-id s3invoke --action "lambda:InvokeFunction" \
    --principal s3.amazonaws.com \
    --source-arn arn:aws:s3:::${BUCKET}

# Attach the S3 -> Lambda notification (edit s3-notification.json first)
aws s3api put-bucket-notification-configuration \
    --bucket ${BUCKET} \
    --notification-configuration file://s3-notification.json

echo "Deployed FeedbackIngestOrchestrator"
