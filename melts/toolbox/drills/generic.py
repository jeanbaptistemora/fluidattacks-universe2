import boto3
from datetime import (
    datetime,
)
from pytz import (  # type: ignore
    UTC,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)


def calculate_days_ago(date: datetime) -> int:
    """
    Return passed days after a provided date

    param: date: provided date to calculate passed days
    """
    passed_days = datetime.utcnow().replace(tzinfo=UTC) - date.replace(
        tzinfo=UTC
    )
    return passed_days.days


def s3_path_exists(
    bucket: str,
    path: str,
    endpoint_url: Optional[str] = None,
) -> bool:
    """
    Return True if provided path exists within a bucket. Else otherwise

    param: bucket: Bucket to work with
    param: path: Path to verify existance within bucket
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client("s3", endpoint_url=endpoint_url)
    kwargs_list_objects: Dict[str, Any] = {
        "Bucket": bucket,
        "Prefix": path,
    }
    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(**kwargs_list_objects):
        return page.get("Contents") is not None
    return False


def get_last_upload(
    bucket: str, path: str, endpoint_url: Optional[str] = None
) -> datetime:
    """
    Get upload date of last uploaded file in a path

    param: bucket: Bucket to work with
    param: path: Path to look for newest file
    param: endpoint_url: aws endpoint to send API requests
    """
    s3_client = boto3.client("s3", endpoint_url=endpoint_url)
    kwargs_list_objects: Dict[str, Any] = {
        "Bucket": bucket,
        "Prefix": path,
    }
    last_modified: datetime = datetime(2000, 1, 1).replace(tzinfo=UTC)
    files_raw: List[Dict[str, Any]]

    paginator = s3_client.get_paginator("list_objects_v2")
    for page in paginator.paginate(**kwargs_list_objects):
        try:
            files_raw = page["Contents"]
        except KeyError:
            break
        for filename in files_raw:
            if last_modified < filename["LastModified"]:
                last_modified = filename["LastModified"]
    return last_modified
