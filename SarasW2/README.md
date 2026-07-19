# Customer Feedback Intelligence Platform — British Airways

Course Project — Build AI with AWS (Weeks 3–5)

An NLP + ML pipeline that ingests British Airways customer reviews, analyzes sentiment and topics
with Amazon Comprehend, predicts CSAT scores with SageMaker Autopilot, generates service-recovery
recommendations with Amazon Bedrock, and exposes it all through a REST API and an Amazon Lex chatbot.

## Architecture

```
S3 (raw reviews) --> Lambda (ingest) --> DynamoDB --> Lambda (Comprehend enrich)
                                                    --> SageMaker Autopilot (CSAT)
                                                    --> Bedrock (recommendations)
DynamoDB --> API Gateway --> dashboard
DynamoDB --> Lex fulfillment Lambda --> chatbot
```

## Repo structure

```
SarasW2/
├── lambda/
│   ├── ingest_orchestrator/   # Week 4 — S3-triggered ingestion into DynamoDB
│   ├── get_feedback/          # Week 4 — API Gateway read endpoint
│   ├── comprehend_enrich/     # Week 5 — sentiment/key phrase/entity enrichment + Bedrock recommendations
│   └── lex_fulfillment/       # Week 5 — Lex bot fulfillment + intent definition
├── infra/
│   ├── template.yaml          # SAM template for API Gateway
│   └── setup-infra.sh         # S3 bucket + DynamoDB table setup
├── notebooks/
│   └── topic_modeling.py      # LDA topic modeling over negative reviews
├── scripts/
│   └── launch_autopilot_job.py
├── requirements.txt
└── README.md
```

## Setup

1. `bash infra/setup-infra.sh` — creates the S3 bucket and `FeedbackRecords` DynamoDB table.
2. `bash lambda/ingest_orchestrator/deploy.sh` — deploys the ingestion Lambda and wires the S3 trigger.
3. Deploy `comprehend_enrich` as a Lambda triggered by a DynamoDB Stream on `FeedbackRecords`.
4. Run `scripts/launch_autopilot_job.py` to train the CSAT model, then deploy the resulting endpoint.
5. `sam build && sam deploy --guided` (from `infra/`) to stand up the API Gateway.
6. Create the `RoboAdvisorBot`-style Lex bot using `lambda/lex_fulfillment/intent-definition.json` and
   point its fulfillment at `lex_fulfillment.py`.

## AWS services used

S3, Lambda, API Gateway, DynamoDB, Amazon Comprehend, SageMaker Autopilot, Amazon Bedrock, Amazon Lex,
CloudWatch, IAM.

## Status

Infrastructure and code scaffolding for Weeks 4–5. Fill in deployment-specific values (account ID,
region, endpoint ARNs) before running against a live AWS account.
