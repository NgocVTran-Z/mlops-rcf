import os
import json
import pandas as pd
import boto3
from io import BytesIO

def main():
    s3 = boto3.client("s3")

    input_bucket = "swo-ngoctran-public"
    input_prefix = "incoming_data/"
    output_prefix = "/opt/ml/processing/output/"

    # ✅ Lấy danh sách file từ biến môi trường
    input_files = json.loads(os.environ.get("INPUT_FILES", "[]"))

    for file in input_files:
        input_key = input_prefix + file
        print(f"📥 Processing {input_key}")

        # Read input
        obj = s3.get_object(Bucket=input_bucket, Key=input_key)
        df = pd.read_csv(BytesIO(obj['Body'].read()), header=None)

        # Transform
        df[0] *= 20

        # Save to local output
        local_output_path = os.path.join(output_prefix, file)
        df.to_csv(local_output_path, index=False, header=False)
        print(f"📤 Saved to {local_output_path}")

if __name__ == "__main__":
    main()
