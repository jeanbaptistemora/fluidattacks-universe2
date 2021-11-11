from bugsnag.notification import (
    Notification,
)
import os
import re


def _remove_nix_hash(path: str) -> str:
    pattern = r"(\/nix\/store\/[a-z0-9]{32}-)"
    result = re.search(pattern, path)
    if not result:
        return path
    return path[result.end(0) :]


def remove_nix_hash(
    notification: Notification,
) -> None:
    notification.stacktrace = [
        {**trace, "file": _remove_nix_hash(trace["file"])}
        for trace in notification.stacktrace
    ]


def add_batch_metadata(
    notification: Notification,
) -> None:
    batch_job_info = {}
    if batch_job_id := os.environ.get("AWS_BATCH_JOB_ID"):
        batch_job_info["batch_job_id"] = batch_job_id
    if job_queue_name := os.environ.get("AWS_BATCH_JQ_NAME"):
        batch_job_info["batch_job_queue"] = job_queue_name

    if batch_job_info:
        notification.add_tab("batch_job_info", batch_job_info)
