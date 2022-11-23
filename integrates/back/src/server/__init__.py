from celery import (
    Celery,
)

BROKER_TRANSPORT_OPTIONS = {
    "region": "us-east-1",
    "polling_interval": 0.3,
    "visibility_timeout": 300,
}
SERVER = Celery(
    "report",
    broker=("sqs://"),
    include=["server.tasks"],
    broker_transport_options=BROKER_TRANSPORT_OPTIONS,
)

if __name__ == "__main__":
    SERVER.start()
