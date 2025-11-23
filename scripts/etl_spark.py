# scripts/etl_spark.py
import yaml
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import sum as _sum

def run_spark_etl(config_path="configs/config.yaml"):
    # Load config
    with open(config_path) as f:
        config = yaml.safe_load(f)

    input_path = config["paths"]["raw_data"]            # e.g. data/raw/transactions.csv
    output_dir = config["paths"]["transformed_dir"]     # a folder for spark csv output
    output_file = config["paths"]["transformed_data"]   # final consolidated CSV path

    # Initialize Spark
    spark = (SparkSession.builder
             .appName("CustomerTransactionETL")
             .config("spark.sql.execution.arrow.enabled", "true")
             .getOrCreate())

    print(f"[PySpark] Reading input: {input_path}")
    df = spark.read.option("header", True).option("inferSchema", True).csv(input_path)

    # Minimal cleaning: drop duplicates
    before = df.count()
    df = df.dropDuplicates()
    after = df.count()
    print(f"[PySpark] Dropped duplicates: {before - after} rows removed")

    # Fill missing numeric values with 0 (only numeric dtypes)
    numeric_cols = [c for c, t in df.dtypes if t in ("int", "double", "long", "float", "bigint")]
    for c in numeric_cols:
        df = df.fillna({c: 0})

    # Example transformation: add total_amount = sum of numeric columns (safe sum)
    if numeric_cols:
        exprs = [col(c) for c in numeric_cols]
        df = df.withColumn("total_amount", sum(exprs))
        print(f"[PySpark] Added 'total_amount' column using numeric cols: {numeric_cols}")
    else:
        print("[PySpark] No numeric columns detected for total_amount; skipping")

    # Write out to CSV (Spark writes part files); we write to a folder then consolidate in driver
    print(f"[PySpark] Writing transformed data to folder: {output_dir}")
    df.coalesce(1).write.option("header", True).mode("overwrite").csv(output_dir)

    # Consolidate the single CSV part file to the configured final CSV path
    # Spark created a file like output_dir/part-*.csv; move it to desired output_file
    import os, glob, shutil
    part_files = glob.glob(os.path.join(output_dir, "part-*.csv"))
    if part_files:
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        shutil.move(part_files[0], output_file)
        # remove any _SUCCESS files and leftover folders
        success_file = os.path.join(output_dir, "_SUCCESS")
        if os.path.exists(success_file):
            os.remove(success_file)
        try:
            # remove directory if empty
            shutil.rmtree(output_dir)
        except Exception:
            pass
        print(f"[PySpark] Consolidated transformed data to {output_file}")
    else:
        print("[PySpark] ERROR: No part file found after Spark write.")

    spark.stop()
    print("[PySpark] ETL finished successfully.")
