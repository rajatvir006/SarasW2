# comprehend_enrich.py
import boto3

comprehend = boto3.client("comprehend")
table = boto3.resource("dynamodb").Table("FeedbackRecords")

def enrich_review(review_id: str, text: str):
    sentiment_resp = comprehend.detect_sentiment(Text=text, LanguageCode="en")
    key_phrases_resp = comprehend.detect_key_phrases(Text=text, LanguageCode="en")
    entities_resp = comprehend.detect_entities(Text=text, LanguageCode="en")

    key_phrases = [kp["Text"] for kp in key_phrases_resp["KeyPhrases"]]
    entities = [{"text": e["Text"], "type": e["Type"]} for e in entities_resp["Entities"]]

    table.update_item(
        Key={"review_id": review_id},
        UpdateExpression="SET sentiment = :s, sentiment_score = :sc, key_phrases = :kp, entities = :e",
        ExpressionAttributeValues={
            ":s": sentiment_resp["Sentiment"],
            ":sc": str(sentiment_resp["SentimentScore"]),
            ":kp": key_phrases,
            ":e": entities,
        },
    )
    return sentiment_resp["Sentiment"]

def lambda_handler(event, context):
    processed = 0
    for record in event["Records"]:
        if record["eventName"] not in ("INSERT", "MODIFY"):
            continue
        new_image = record["dynamodb"]["NewImage"]
        review_id = new_image["review_id"]["S"]
        text = new_image["raw_text"]["S"]
        enrich_review(review_id, text)
        processed += 1
    return {"processed": processed}
