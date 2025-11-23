# aws/lambda_handler.py
"""
Simulated AWS Lambda handler that triggers the PySpark ETL.
"""
from scripts.etl_spark import run_spark_etl

def lambda_handler(event=None, context=None):
    print("[Lambda] Starting ETL pipeline (simulated Lambda)...")
    # event can be used to pass filenames or parameters if desired
    config_path = "configs/config.yaml"
    run_spark_etl(config_path)
    print("[Lambda] ETL pipeline completed.")
