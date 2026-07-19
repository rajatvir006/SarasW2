# get_feedback.py
import json
import boto3

table = boto3.resource("dynamodb").Table("FeedbackRecords")

def lambda_handler(event, context):
    review_id = event["pathParameters"]["review_id"]
    resp = table.get_item(Key={"review_id": review_id})
    item = resp.get("Item")
    if not item:
        return {"statusCode": 404, "body": json.dumps({"error": "not found"})}
    return {"statusCode": 200, "body": json.dumps(item, default=str)}
