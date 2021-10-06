# pylint: disable=invalid-name
"""
This migration searches for evidences without extension
and appends it to them, deleting the old file without extension

Execution Time:    2021-09-28 at 16:14:02 UTC-5
Finalization Time: 2021-09-28 at 18:51:11 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from botocore.exceptions import (
    ClientError,
)
from context import (
    FI_AWS_S3_BUCKET as EVIDENCES_BUCKET,
)
from custom_exceptions import (
    FindingNotFound,
)
from findings import (
    dal as findings_dal,
    domain as findings_domain,
)
from groups import (
    domain as groups_domain,
)
from magic import (
    Magic,
)
import os
from s3.operations import (
    aio_client,
    download_file,
    list_files,
    remove_file,
)
import tempfile
import time
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Union,
)

PROD: bool = True


async def upload_file(
    bucket: str, file_object: object, file_name: str
) -> bool:
    success = False
    async with aio_client() as client:
        try:
            await client.upload_fileobj(
                file_object,
                bucket,
                file_name,
            )
            success = True
        except ClientError as ex:
            print(f"Error occurred uploading file: {ex}")
    return success


async def append_extensions(  # pylint: disable=too-many-locals
    directory: str, full_name: str
) -> None:
    target_extensions = [
        "image/gif",
        "image/png",
        "image/jpeg",
        "application/x-empty",
        "text/x-python",
        "application/csv",
        "text/csv",
        "text/plain",
    ]
    target_name = os.path.join(directory, os.path.basename(full_name))
    evidence_id = os.path.basename(full_name).split("-")[-1]
    if not os.path.isdir(target_name):
        await download_file(EVIDENCES_BUCKET, full_name, target_name)
        mime = Magic(mime=True)
        mime_type = mime.from_file(target_name)
        if mime_type in target_extensions:

            print(f"Found evidence file without extension: {full_name}")
            # Determining finding id and index
            # that corresponds to this evidence
            finding_id = full_name.split("/")[1]
            try:
                finding = await findings_domain.get_finding(finding_id)
            except FindingNotFound:
                print(f"The finding {finding_id} doesn't exist")
                return
            files = finding.get("files", [])
            evidence: Union[Dict[str, str], List[Optional[Any]]] = next(
                (item for item in files if item["name"] == evidence_id), []
            )
            try:
                index = files.index(evidence)
            except ValueError:
                print(f"Evidence {evidence_id} not in finding {finding_id}")
                return
            # Choosing and appending the appropiate extension
            extension = {
                "image/gif": ".gif",
                "image/jpeg": ".jpg",
                "image/png": ".png",
                "application/x-empty": ".exp",
                "text/x-python": ".exp",
                "application/csv": ".csv",
                "text/csv": ".csv",
                "text/plain": ".txt",
            }[mime_type]
            upload_name = full_name + extension
            print(f"File with appended extension will be: {upload_name}")
            if PROD:
                # Upload file with extension, update its name in the db
                # and delete the old file
                with open(
                    target_name, mode="rb", encoding=None
                ) as target_file:
                    success = await upload_file(
                        EVIDENCES_BUCKET, target_file, upload_name
                    )
                    file_url = f"{os.path.basename(full_name)}{extension}"
                    await findings_dal.update(
                        finding_id,
                        {
                            f"files[{index}].file_url": file_url,
                        },
                    )
                    print(f"{upload_name} upload successful: {success}")
                    if success:
                        await remove_file(EVIDENCES_BUCKET, full_name)
                        print(f"{full_name} file removed")


async def process_evidences(group: str) -> None:
    with tempfile.TemporaryDirectory() as directory:
        os.makedirs(directory, exist_ok=True)
        for key in await list_files(EVIDENCES_BUCKET, group):
            _, extension = os.path.splitext(key)
            if extension == "":
                await append_extensions(directory, key)


async def main() -> None:
    all_groups = await groups_domain.get_alive_group_names()
    await collect(process_evidences(group) for group in all_groups)


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
