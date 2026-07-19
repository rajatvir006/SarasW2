# lex_fulfillment.py
import boto3

table = boto3.resource("dynamodb").Table("FeedbackRecords")

def lambda_handler(event, context):
    slots = event["sessionState"]["intent"]["slots"]
    topic = slots["Topic"]["value"]["interpretedValue"]

    # In production: query a topic-indexed GSI instead of a full scan
    items = table.scan()["Items"]
    matches = [i for i in items if topic.lower() in " ".join(i.get("key_phrases", [])).lower()]
    negative = [m for m in matches if m.get("sentiment") == "NEGATIVE"]

    message = (
        f"Found {len(matches)} reviews mentioning '{topic}', "
        f"{len(negative)} of them negative."
    )

    return {
        "sessionState": {
            "dialogAction": {"type": "Close"},
            "intent": {"name": "GetFeedbackInsight", "state": "Fulfilled"},
        },
        "messages": [{"contentType": "PlainText", "content": message}],
    }
