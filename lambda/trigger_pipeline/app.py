import json
import boto3
import uuid
import os

sagemaker = boto3.client("sagemaker")

def lambda_handler(event, context):
    try:
        print("🟢 Lambda is running.")
        print("📨 Event received:", event)

        body = json.loads(event['body'])
        pipeline = body.get("pipeline")
        params = body.get("params", {})

        if pipeline != "preprocessing_kmeans":
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Unsupported pipeline"})
            }

        job_name = f"preprocess-kmeans-{uuid.uuid4().hex[:8]}"
        input_files = params.get("input_files", [])

        # Read environment variables
        role_arn = os.environ["SAGEMAKER_ROLE_ARN"]
        image_uri = os.environ["PROCESSING_IMAGE_URI"]
        script_s3 = os.environ["SCRIPT_S3_URI"]
        output_s3 = os.environ["OUTPUT_S3_PATH"]

        print("📦 Job Name:", job_name)
        print("📁 Input files:", input_files)
        print("📜 Script S3:", script_s3)
        print("📤 Output S3:", output_s3)

        sagemaker.create_processing_job(
            ProcessingJobName=job_name,
            RoleArn=role_arn,
            AppSpecification={
                "ImageUri": image_uri,
                "ContainerEntrypoint": ["python3", "/opt/ml/processing/code/preprocessing_kmeans.py"]
            },
            ProcessingInputs=[
                {
                    "InputName": "code",
                    "S3Input": {
                        "S3Uri": script_s3,
                        "LocalPath": "/opt/ml/processing/code",
                        "S3DataType": "S3Prefix",
                        "S3InputMode": "File"
                    }
                }
            ],
            ProcessingOutputConfig={
                "Outputs": [
                    {
                        "OutputName": "output",
                        "S3Output": {
                            "S3Uri": output_s3,
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
                "INPUT_FILES": json.dumps(input_files)
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
