import os
import json
import pandas as pd
import boto3
from io import BytesIO

# # Load config
# with open("config/global_config.json") as f:
#     global_config = json.load(f)

# with open("pipelines/01_preprocessing_kmeans/config.json") as f:
#     local_config = json.load(f)

# config = {**global_config, **local_config}


# load config
with open("/opt/ml/processing/code/config/global_config.json") as f:
    global_config = json.load(f)

with open("/opt/ml/processing/code/pipelines/01_preprocessing_kmeans/config.json") as f:
    local_config = json.load(f)

config = {**global_config, **local_config}



def main():
    s3 = boto3.client("s3")

    input_bucket = config["bucket_name"]
    input_prefix = config["incoming_prefix"]
    output_prefix = "/opt/ml/processing/output/"

    input_files = json.loads(os.environ.get("INPUT_FILES", "[]"))

    for file in input_files:
        input_key = input_prefix + file
        print(f"📥 Processing {input_key}")

        try:
            obj = s3.get_object(Bucket=input_bucket, Key=input_key)
        except s3.exceptions.NoSuchKey:
            print(f"❌ File not found: {input_key}, skipping.")
            continue

        df = pd.read_csv(BytesIO(obj['Body'].read()), header=None)
        df[0] = df[0].astype(float) * 2

        local_output_path = os.path.join(output_prefix, file)
        df.to_csv(local_output_path, index=False, header=False)
        print(f"📤 Saved to {local_output_path}")

if __name__ == "__main__":
    main()
