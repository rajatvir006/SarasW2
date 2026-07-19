# launch_autopilot_job.py
import boto3
import time

sm = boto3.client("sagemaker")

job_name = f"ba-csat-autopilot-{int(time.time())}"

response = sm.create_auto_ml_job(
    AutoMLJobName=job_name,
    InputDataConfig=[{
        "DataSource": {
            "S3DataSource": {
                "S3DataType": "S3Prefix",
                "S3Uri": "s3://ba-feedback-platform-rajatvir/processed/training_data.csv",
            }
        },
        "TargetAttributeName": "csat_score",
    }],
    OutputDataConfig={"S3OutputPath": "s3://ba-feedback-platform-rajatvir/models/"},
    ProblemType="Regression",
    AutoMLJobObjective={"MetricName": "MSE"},
    RoleArn="arn:aws:iam::123456789012:role/SageMakerAutopilotRole",
)

print("Started:", job_name)


def check_job_status(job_name: str):
    status = sm.describe_auto_ml_job(AutoMLJobName=job_name)
    print(status["AutoMLJobStatus"], status.get("BestCandidate", {}).get("FinalAutoMLJobObjectiveMetric"))
    return status
