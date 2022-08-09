import boto3
from celery import (
    Celery,
)
from kombu.utils.url import (
    safequote,
)
import os

AWS_CREDENTIALS = boto3.Session().get_credentials()
BROKER_TRANSPORT_OPTIONS = {
    "region": "us-east-1",
    "polling_interval": 0.3,
    "predefined_queues": {
        "celery": {
            "url": (
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/skims-report-queue"
            ),
            "access_key_id": AWS_CREDENTIALS.access_key,
            "secret_access_key": AWS_CREDENTIALS.secret_key,
        },
        "skims-report-queue": {
            "url": (
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/skims-report-queue"
            ),
            "access_key_id": AWS_CREDENTIALS.access_key,
            "secret_access_key": AWS_CREDENTIALS.secret_key,
        },
    },
}
app = Celery(
    "report",
    broker=(
        f"sqs://{safequote(AWS_CREDENTIALS.access_key)}:"
        f"{safequote(AWS_CREDENTIALS.secret_key)}@"
    ),
    include=["server.tasks"],
    broker_transport_options=BROKER_TRANSPORT_OPTIONS,
    s3_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
    s3_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
    s3_bucket="skims.data",
    s3_base_path="celery_result_backend/",
    s3_region="us-east-1",
    backend="s3",
)

if __name__ == "__main__":
    app.start()
