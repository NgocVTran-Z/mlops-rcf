import os
import json
import pandas as pd

from shared.io.s3_parquet_loader import load_parquet_files_from_folders
from shared.utils.dataframe_utils import print_dataframe_shape

# Load config
with open("/opt/ml/processing/code/config/global_config.json") as f:
    global_config = json.load(f)
with open("/opt/ml/processing/code/pipelines/01_preprocessing_kmeans/config.json") as f:
    local_config = json.load(f)
config = {**global_config, **local_config}


def main():
    print("🧪 ENVIRONMENT VARIABLES DUMP:")
    for key, value in os.environ.items():
        print(f"🔹 {key} = {value}")

    input_folders = json.loads(os.environ.get("INPUT_FILES", "[]"))
    speed_tags = json.loads(os.environ.get("SPEED_TAGS", "[]"))

    print("📌 Speed Tags received:", speed_tags)

    df = load_parquet_files_from_folders(
        bucket=config["bucket_name"],
        prefix=config["incoming_prefix"],
        folders=input_folders
    )

    print_dataframe_shape(df)


if __name__ == "__main__":
    main()
