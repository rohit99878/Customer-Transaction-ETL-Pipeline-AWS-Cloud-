# scripts/run_pipeline_aws.py
from aws.s3_simulator import S3Simulator
from aws.redshift_simulator import RedshiftSimulator
from aws.lambda_handler import lambda_handler
import yaml
import os

# load config to get paths
with open("configs/config.yaml") as f:
    config = yaml.safe_load(f)

RAW_LOCAL = config["paths"]["raw_data"]            # data/raw/transactions.csv
S3_RAW_KEY = "raw/transactions.csv"
S3_TRANSFORMED_KEY = "transformed/transactions_final.csv"

def run():
    # init simulators
    s3 = S3Simulator()
    redshift = RedshiftSimulator()

    # Step 1: Upload raw data to S3 simulator
    print("[Runner] Uploading raw CSV to simulated S3...")
    s3.upload_file(RAW_LOCAL, S3_RAW_KEY)

    # Step 2: Trigger Lambda (which runs PySpark ETL)
    print("[Runner] Triggering simulated Lambda ETL...")
    lambda_handler()

    # Step 3: Simulate loading transformed file into Redshift
    print("[Runner] Simulating Redshift COPY from S3...")
    redshift.copy_from_s3("customer_transactions", f"s3://bucket/{S3_TRANSFORMED_KEY}")

    # Step 4: Run sample analytics queries (simulated)
    redshift.run_analytics_queries()

if __name__ == "__main__":
    run()
