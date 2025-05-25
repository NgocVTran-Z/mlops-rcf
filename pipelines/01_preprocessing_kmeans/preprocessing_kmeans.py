import pandas as pd
import boto3
import argparse
import os
from io import BytesIO

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_files', nargs='+', required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    s3 = boto3.client("s3")

    input_bucket = "swo-ngoctran-public"
    input_prefix = "incoming_data/"
    output_prefix = "/opt/ml/processing/output/"

    for file in args.input_files:
        input_key = input_prefix + file
        print(f"📥 Processing {input_key}")

        # Read input
        obj = s3.get_object(Bucket=input_bucket, Key=input_key)
        df = pd.read_csv(BytesIO(obj['Body'].read()), header=None)

        # Transform
        df[0] *= 10

        # Save to local output
        local_output_path = os.path.join(output_prefix, file)
        df.to_csv(local_output_path, index=False, header=False)
        print(f"📤 Saved to {local_output_path}")

if __name__ == "__main__":
    main()
