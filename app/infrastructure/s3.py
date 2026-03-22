import boto3
from app.config import *

s3 = boto3.client(
    "s3",
    endpoint_url=S3_ENDPOINT,
    aws_access_key_id=S3_ACCESS_KEY,
    aws_secret_access_key=S3_SECRET_KEY,
)

class S3Service:
    def upload_fileobj(self, file, key: str):
        s3.upload_fileobj(file, S3_BUCKET, key)

    def download_file(self, key: str, path: str):
        s3.download_file(S3_BUCKET, key, path)

    def generate_presigned_url(self, key: str):
        return s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": S3_BUCKET, "Key": key},
            ExpiresIn=3600
        )