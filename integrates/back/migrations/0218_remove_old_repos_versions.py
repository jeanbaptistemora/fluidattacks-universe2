# pylint: disable=invalid-name
"""
Remove objects from bucket

remove all previous versions of objects, along with
objects that have already been marked as deleted

Execution Time: 2022-05-25 at 01:52:49 UTCUTC
Finalization Time: 2002-05-25 at 06:22:52 UTCUTC
"""

from aioextensions import (
    collect,
    run,
)
from batch_dispatch.utils.s3 import (
    SESSION,
)
from collections.abc import (
    Coroutine,
)
from more_itertools import (
    chunked,
)
import time


async def main() -> None:
    async with SESSION.client(service_name="s3") as client:
        next_version_id = None
        next_key_marker = None
        objects_to_delete: list[tuple[str, str]] = []
        while True:
            response = await client.list_object_versions(
                Bucket="continuous-repositories",
                **(
                    {
                        "VersionIdMarker": next_version_id,
                        "KeyMarker": next_key_marker,
                    }
                    if next_version_id is not None
                    else {}
                ),
            )
            objects_to_delete = [
                *objects_to_delete,
                *[
                    (obj["Key"], obj["VersionId"])
                    for obj in response.get("DeleteMarkers", [])
                ],
            ]
            objects_to_delete = [
                *objects_to_delete,
                *[
                    (obj["Key"], obj["VersionId"])
                    for obj in response.get("Versions", [])
                    if obj["IsLatest"] is False
                    or not obj["Key"].endswith(".tar.gz")
                ],
            ]
            if (
                len(objects_to_delete) > 10000
                or "NextVersionIdMarker" not in response
            ):
                async with SESSION.resource("s3") as s3:
                    bucket = await s3.Bucket("continuous-repositories")
                    tasks: list[Coroutine] = [
                        bucket.delete_objects(
                            Delete={
                                "Objects": [
                                    {"Key": key, "VersionId": version_id}
                                    for key, version_id in set_objects
                                ],
                                "Quiet": True,
                            },
                        )
                        for set_objects in chunked(objects_to_delete, 1000)
                    ]
                    await collect(tasks)
                    objects_to_delete = []

            if "NextVersionIdMarker" not in response:
                next_version_id = None
                break

            next_version_id = response["NextVersionIdMarker"]
            next_key_marker = response["NextKeyMarker"]


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
