import json
import boto3
import uuid

sagemaker = boto3.client("sagemaker")

def lambda_handler(event, context):
    body = json.loads(event['body'])

    pipeline = body.get("pipeline")
    params = body.get("params", {})

    if pipeline != "preprocessing_kmeans":
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Unsupported pipeline"})
        }

    job_name = f"preprocess-kmeans-{uuid.uuid4().hex[:8]}"
    script_uri = "s3://swo-ngoctran-public/jobs/preprocessing_kmeans.py"

    arguments = []
    if "input_files" in params:
        arguments += ["--input_files"] + params["input_files"]

    response = sagemaker.create_processing_job(
        ProcessingJobName=job_name,
        RoleArn="arn:aws:iam::975049948583:role/AmazonSageMaker-ExecutionRole-20250518T181754",
        AppSpecification={
            "ImageUri": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3",
            "ScriptUri": script_uri
        },
        ProcessingInputs=[],
        ProcessingOutputConfig={
            "Outputs": [
                {
                    "OutputName": "output",
                    "S3Output": {
                        "S3Uri": "s3://swo-ngoctran-public/inference_result/",
                        "LocalPath": "/opt/ml/processing/output",
                        "S3UploadMode": "EndOfJob"
                    }
                }
            ]
        },
        StoppingCondition={"MaxRuntimeInSeconds": 3600},
        Arguments=arguments
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": f"✅ Triggered job: {job_name}",
            "job_name": job_name
        })
    }
