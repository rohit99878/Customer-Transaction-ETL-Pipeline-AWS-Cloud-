# scripts/extract.py
import yaml
import pandas as pd

def extract(config_path="configs/config.yaml"):
    with open(config_path) as f:
        config = yaml.safe_load(f)
    raw_path = config["paths"]["raw_data"]
    print(f"[Extract] Loading raw data from {raw_path}")
    df = pd.read_csv(raw_path)
    print(f"[Extract] Loaded {df.shape[0]} rows and {df.shape[1]} columns")
    return df
