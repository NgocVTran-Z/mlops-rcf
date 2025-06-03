import os
import json
import pandas as pd
import boto3
from io import BytesIO

# Load config
with open("/opt/ml/processing/code/config/global_config.json") as f:
    global_config = json.load(f)

with open("/opt/ml/processing/code/pipelines/01_preprocessing_kmeans/config.json") as f:
    local_config = json.load(f)

config = {**global_config, **local_config}

def main():
    s3 = boto3.client("s3")

    input_bucket = config["bucket_name"]
    input_prefix = config["incoming_prefix"]

    input_folders = json.loads(os.environ.get("INPUT_FILES", "[]"))
    speed_tags = json.loads(os.environ.get("SPEED_TAGS", "[]"))

    print("📌 Speed Tags received:", speed_tags)

    total_files = 0

    for folder in input_folders:
        prefix = input_prefix + folder.strip("/") + "/"
        print(f"🔍 Scanning folder: s3://{input_bucket}/{prefix}")

        response = s3.list_objects_v2(Bucket=input_bucket, Prefix=prefix)
        parquet_keys = [
            obj["Key"]
            for obj in response.get("Contents", [])
            if obj["Key"].endswith(".parquet")
        ]

        if not parquet_keys:
            print(f"⚠️ No .parquet files found in {prefix}")
            continue

        for key in parquet_keys:
            print(f"📥 Reading file: s3://{input_bucket}/{key}")
            try:
                obj = s3.get_object(Bucket=input_bucket, Key=key)
                df = pd.read_parquet(BytesIO(obj["Body"].read()))
                print(f"✅ File shape: {df.shape}")
                total_files += 1
            except Exception as e:
                print(f"❌ Failed to read {key}: {e}")

    print(f"📊 Total .parquet files processed: {total_files}")

if __name__ == "__main__":
    main()
