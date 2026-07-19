# lambda_function.py — FeedbackIngestOrchestrator
import json
import csv
import io
import uuid
import boto3
from datetime import datetime, timezone

s3 = boto3.client("s3")
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("FeedbackRecords")

def lambda_handler(event, context):
    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    obj = s3.get_object(Bucket=bucket, Key=key)
    body = obj["Body"].read().decode("utf-8")

    reader = csv.DictReader(io.StringIO(body))
    written = 0

    with table.batch_writer() as batch:
        for row in reader:
            review_text = row.get("review") or row.get("text")
            if not review_text:
                continue
            batch.put_item(Item={
                "review_id": str(uuid.uuid4()),
                "raw_text": review_text,
                "sentiment": "PENDING",       # updated by Week 5 Comprehend step
                "csat_prediction": None,       # updated by Week 5 SageMaker step
                "created_at": datetime.now(timezone.utc).isoformat(),
            })
            written += 1

    return {
        "statusCode": 200,
        "body": json.dumps({"records_written": written, "source_key": key}),
    }
