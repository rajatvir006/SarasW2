# bedrock_recommend.py
import boto3

bedrock = boto3.client("bedrock-runtime", region_name="us-east-1")

def generate_recommendation(sentiment: str, key_phrases: list, csat_score: float) -> str:
    prompt = (
        f"A British Airways customer review was classified as {sentiment} "
        f"(predicted CSAT: {csat_score}). Key phrases: {', '.join(key_phrases)}. "
        "In 2-3 sentences, suggest one concrete, actionable service-recovery or "
        "improvement step for the operations team."
    )
    response = bedrock.converse(
        modelId="anthropic.claude-3-5-sonnet-20241022-v2:0",
        messages=[{"role": "user", "content": [{"text": prompt}]}],
        inferenceConfig={"maxTokens": 200, "temperature": 0.4},
    )
    return response["output"]["message"]["content"][0]["text"]
