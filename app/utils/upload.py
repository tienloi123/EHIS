import boto3

from app.core import settings


def get_minio_client():
    return boto3.client(
        's3',
        endpoint_url=settings.OBJECT_STORAGE_ENDPOINT,  # MinIO endpoint
        aws_access_key_id=settings.OBJECT_STORAGE_ACCESS_KEY_ID,
        aws_secret_access_key=settings.OBJECT_STORAGE_SECRET_ACCESS_KEY,
        region_name=settings.OBJECT_STORAGE_REGION)

def get_minio_bucket_name():
    return settings.OBJECT_STORAGE_BUCKET_NAME
