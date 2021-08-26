import aioboto3
import asyncio
import boto3
from contextlib import (
    suppress,
)
import fnmatch
import logging
from more_itertools import (
    flatten,
)
import os
import sys
from typing import (
    Any,
    Optional,
    Set,
)

logging.basicConfig(format="# [%(levelname)s] %(message)s")
LOG = logging.getLogger("gatsby_sync")
LOG.setLevel(logging.INFO)


PUBLIC = sys.argv[1]
BUCKET = sys.argv[2]

client = boto3.client("s3")


def list_s3_objects(
    next_token: Optional[str] = None, developer: Optional[str] = None
) -> Set[str]:
    objects = set()
    if next_token:
        response = client.list_objects_v2(
            Bucket=BUCKET,
            MaxKeys=100,
            ContinuationToken=next_token,
        )
    else:
        response = client.list_objects_v2(Bucket=BUCKET, MaxKeys=10)

    for obj in response.get("Contents", list()):
        key: str = obj["Key"]
        if developer:
            if key.startswith(developer):
                objects.add(obj["Key"])
        else:
            objects.add(obj["Key"])
    if next_token := response.get("NextContinuationToken"):
        objects.update(list_s3_objects(next_token, developer))
    return objects


def list_local(path: str) -> Set[str]:
    path = f"{path}/" if not path.endswith("/") else path
    files_set = set()
    for directory, _, files in os.walk(path):
        for file in files:
            f_path = os.path.join(directory, file)
            files_set.add(f_path.replace(path, ""))
    return files_set


async def upload(
    s3_client: Any,
    bucket: str,
    staging_path: str,
    filename: str,
    developer: Optional[str] = None,
) -> str:
    content_encodings = {
        "css": "gzip",
        "html": "gzip",
        "js": "gzip",
        "png": "identity",
        "svg": "identity",
    }
    content_types = {
        "css": "text/css",
        "html": "text/html",
        "js": "application/javascript",
        "png": "image/png",
        "svg": "image/svg+xml",
    }
    filename = f"{developer}/{filename}" if developer else filename
    file_extension = filename.split(".")[-1]
    args = {}
    if file_extension in content_encodings:
        args = {
            "ACL": "private",
            "ContentEncoding": content_encodings[file_extension],
            "ContentType": content_types[file_extension],
        }
    with open(staging_path, "rb") as spfp:
        await s3_client.upload_fileobj(spfp, bucket, filename, ExtraArgs=args)
        return filename


async def delete_files(s3_client: Any, files: Set[str]) -> None:
    if files:
        for file in files:
            LOG.info("Delete %s", file)
        await s3_client.delete_objects(
            Bucket=BUCKET,
            Delete={
                "Objects": [{"Key": key} for key in files],
                "Quiet": False,
            },
        )


async def main() -> None:
    developer = None
    with suppress(IndexError):
        developer = sys.argv[3]
    local_files = list_local(PUBLIC)
    uploads = [
        fnmatch.filter(local_files, "*.js"),
        fnmatch.filter(local_files, "*.js.map"),
        fnmatch.filter(local_files, "*.json"),
        fnmatch.filter(local_files, "*.txt"),
        fnmatch.filter(local_files, "*.css"),
        fnmatch.filter(local_files, "*.scss"),
        fnmatch.filter(local_files, "*.html"),
    ]
    all_uploads = set(flatten(uploads))
    no_upload = local_files.difference(all_uploads)
    uploads.append(list(no_upload))

    if developer:
        _local_files = {f"{developer}/{_file}" for _file in local_files}
    else:
        _local_files = local_files

    bucket_files = list_s3_objects(developer=developer)
    files_to_delete = bucket_files.difference(_local_files)

    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        for files_to_upload in uploads:
            futures = [
                upload(
                    s3_client,
                    BUCKET,
                    f"{PUBLIC}/{file}",
                    file,
                    developer=developer,
                )
                for file in files_to_upload
            ]
            for upp in asyncio.as_completed(futures):
                LOG.info("Uploaded %s", await upp)
        await delete_files(s3_client, files_to_delete)


asyncio.run(main())
