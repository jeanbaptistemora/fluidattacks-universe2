from celery import Celery
from kombu.utils.url import safequote
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
)

if __name__ == "__main__":
    app.start()
