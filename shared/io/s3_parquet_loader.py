import boto3
import pandas as pd
from io import BytesIO

def load_parquet_files_from_folders(bucket: str, prefix: str, folders: list) -> pd.DataFrame:
    """
    Load and concatenate all .parquet files from a list of folders under a given S3 prefix.
    Return empty DataFrame if nothing found.
    """
    s3 = boto3.client("s3")
    df_list = []

    for folder in folders:
        folder_prefix = prefix + folder.strip("/") + "/"
        response = s3.list_objects_v2(Bucket=bucket, Prefix=folder_prefix)

        parquet_keys = [
            obj["Key"] for obj in response.get("Contents", [])
            if obj["Key"].endswith(".parquet")
        ]

        if not parquet_keys:
            print(f"⚠️ No .parquet files found in s3://{bucket}/{folder_prefix}")
            continue

        for key in parquet_keys:
            print(f"📥 Reading: s3://{bucket}/{key}")
            try:
                obj = s3.get_object(Bucket=bucket, Key=key)
                df = pd.read_parquet(BytesIO(obj["Body"].read()))
                df_list.append(df)
            except Exception as e:
                print(f"❌ Failed to read {key}: {e}")

    if not df_list:
        return pd.DataFrame()

    combined_df = pd.concat(df_list, ignore_index=True)
    print(f"✅ Combined shape: {combined_df.shape}")
    print(f"Columns: {combined_df.columns}")
    return combined_df
