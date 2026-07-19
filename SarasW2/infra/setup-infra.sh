#!/bin/bash
# setup-infra.sh — creates the S3 bucket, key prefixes, and DynamoDB table
set -e

BUCKET="ba-feedback-platform-rajatvir"
REGION="ap-south-1"

# S3 bucket + prefixes
aws s3 mb s3://$BUCKET --region $REGION
aws s3api put-object --bucket $BUCKET --key raw/
aws s3api put-object --bucket $BUCKET --key processed/
aws s3api put-object --bucket $BUCKET --key models/

# DynamoDB table
aws dynamodb create-table \
    --table-name FeedbackRecords \
    --attribute-definitions AttributeName=review_id,AttributeType=S \
    --key-schema AttributeName=review_id,KeyType=HASH \
    --billing-mode PAY_PER_REQUEST \
    --region $REGION

echo "Infra setup complete: s3://$BUCKET and DynamoDB table FeedbackRecords"
