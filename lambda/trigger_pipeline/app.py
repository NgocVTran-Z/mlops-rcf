import json
import boto3
import uuid

sagemaker = boto3.client("sagemaker")

def lambda_handler(event, context):
    try:
        print("Received event:", json.dumps(event))

        body = json.loads(event['body'])
        pipeline = body.get("pipeline")
        params = body.get("params", {})

        if pipeline != "preprocessing_kmeans":
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Unsupported pipeline"})
            }

        job_name = f"preprocess-kmeans-{uuid.uuid4().hex[:8]}"

        sagemaker.create_processing_job(
            ProcessingJobName=job_name,
            RoleArn="arn:aws:iam::975049948583:role/AmazonSageMaker-ExecutionRole-20250518T181754",
            AppSpecification={
                "ImageUri": "683313688378.dkr.ecr.us-east-1.amazonaws.com/sagemaker-scikit-learn:0.23-1-cpu-py3"
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
            ProcessingResources={
                "ClusterConfig": {
                    "InstanceCount": 1,
                    "InstanceType": "ml.m5.large",
                    "VolumeSizeInGB": 10
                }
            },
            StoppingCondition={
                "MaxRuntimeInSeconds": 3600
            },
            Environment={
                "INPUT_FILES": json.dumps(params.get("input_files", []))
            }
        )

        return {
            "statusCode": 200,
            "body": json.dumps({"message": f"Triggered job {job_name}"})
        }

    except Exception as e:
        print("💥 Error:", str(e))
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal error", "details": str(e)})
        }
