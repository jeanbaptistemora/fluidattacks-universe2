from celery import (
    Celery,
)
from kombu.utils.url import (
    safequote,
)
import os

BROKER_TRANSPORT_OPTIONS = {
    "region": "us-east-1",
    "polling_interval": 0.3,
    "predefined_queues": {
        "celery": {
            "url": (
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/skims-report-queue"
            ),
            "access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
        "skims-report-queue": {
            "url": (
                "https://sqs.us-east-1.amazonaws.com/"
                "205810638802/skims-report-queue"
            ),
            "access_key_id": os.environ["AWS_ACCESS_KEY_ID"],
            "secret_access_key": os.environ["AWS_SECRET_ACCESS_KEY"],
        },
    },
}
app = Celery(
    "report",
    broker=(
        f"sqs://{safequote(os.environ['AWS_ACCESS_KEY_ID'])}:"
        f"{safequote(os.environ['AWS_SECRET_ACCESS_KEY'])}@"
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
