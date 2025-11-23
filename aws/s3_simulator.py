# aws/s3_simulator.py
import shutil
import os

class S3Simulator:
    def __init__(self, bucket_folder="data/s3_bucket/"):
        self.bucket_folder = bucket_folder
        os.makedirs(self.bucket_folder, exist_ok=True)

    def upload_file(self, local_path, s3_key):
        dest = os.path.join(self.bucket_folder, s3_key)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(local_path, dest)
        print(f"[S3 Simulator] Uploaded {local_path} -> s3://bucket/{s3_key}")

    def download_file(self, s3_key, local_path):
        src = os.path.join(self.bucket_folder, s3_key)
        shutil.copy(src, local_path)
        print(f"[S3 Simulator] Downloaded s3://bucket/{s3_key} -> {local_path}")
