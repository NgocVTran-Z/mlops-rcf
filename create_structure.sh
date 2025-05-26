#!/bin/bash

# create all folders
mkdir -p config

mkdir -p pipelines/01_preprocessing_kmeans
mkdir -p pipelines/02_train_kmeans
mkdir -p pipelines/03_preprocessing_rcf
mkdir -p pipelines/04_train_rcf
mkdir -p pipelines/05_inference_batch
mkdir -p pipelines/06_inference_realtime
mkdir -p pipelines/07_deploy_endpoint

mkdir -p lambda/trigger_pipeline
mkdir -p api_gateway
mkdir -p scripts
mkdir -p .github/workflows

touch template.yaml
touch samconfig.toml
touch lambda/trigger_pipeline/app.py
touch lambda/trigger_pipeline/requirements.txt
touch .github/workflows/push_preprocessing_kmeans.yaml


touch pipelines/01_preprocessing_kmeans/preprocessing_kmeans.py
touch pipelines/01_preprocessing_kmeans/input_files.json




