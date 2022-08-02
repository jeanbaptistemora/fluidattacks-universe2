# pylint: disable=invalid-name
"""
This migration delete the duplicated evidences on S3
for unittesting
Execution Time:    2020-11-13 at 12:08:40 UTC-05
Finalization Time: 2020-11-13 at 12:31:53 UTC-05
"""
from aioextensions import (
    collect,
    in_thread,
    run,
)
from botocore.exceptions import (
    ClientError,
)
import logging
import logging.config
import os
from s3.resource import (
    get_s3_resource,
)
from settings import (
    LOGGING,
)
import time
from typing import (
    List,
)

logging.config.dictConfig(LOGGING)

# Constants
BUCKET = "fluidintegrates.evidences"
LOGGER = logging.getLogger(__name__)
STAGE = os.environ["STAGE"]


async def get_all_project_evidences(name: str) -> List[str]:
    client = await get_s3_resource()
    continuation_token = None
    key_list: List[str] = []
    while True:
        if continuation_token:
            resp = await client.list_objects_v2(
                Bucket=BUCKET,
                Prefix=name,
                ContinuationToken=continuation_token,
            )
        else:
            resp = await client.list_objects_v2(Bucket=BUCKET, Prefix=name)
        key_list += [item["Key"] for item in resp.get("Contents", [])]
        if not resp.get("IsTruncated"):
            break
        continuation_token = resp.get("NextContinuationToken")
    return key_list


async def remove_file(name: str) -> int:
    print(f"[INFO] Deleting evidence {name}")
    success = False
    client = await get_s3_resource()
    try:
        response = await client.delete_object(Bucket=BUCKET, Key=name)
        resp_code = response["ResponseMetadata"]["HTTPStatusCode"]
        success = resp_code in [200, 204]
    except ClientError as ex:
        LOGGER.exception(ex, extra={"extra": locals()})
    return success


async def main() -> None:
    print("[INFO] starting migration 0034")
    all_evidences = await get_all_project_evidences("unittesting")
    mock_findings = [
        "988493279",  # findings on dev
        "422286126",  # findings on dev
        "436992569",  # findings on dev
        "463461507",  # findings on dev
        "463558592",  # findings on dev
        "457497316",  # findings on dev
        "769755028",  # findings on prod
        "639056172",  # findings on prod
        "645240449",  # findings on prod
        "968394513",  # findings on prod
        "901143918",  # findings on prod
        "654626578",  # findings on prod
        "777490716",  # findings on prod
        "771151388",  # findings on prod
        "890102429",  # findings on prod
        "677101109",  # findings on prod
        "890190724",  # findings on prod
    ]
    evidences: List[str] = []
    for evidence in all_evidences:
        if evidence.split("/")[1] not in mock_findings:
            evidences.append(evidence)
    evidences.sort()

    if STAGE == "test":
        results = await collect(
            [
                in_thread(print, f"[INFO] Evidence {evidence} will be deleted")
                for evidence in evidences
            ]
        )
        print("[INFO] Total evidences to delete: " f"{len(evidences)}")
        print("[INFO] migration 0031 test finished")

    else:
        results = await collect(
            [await in_thread(remove_file, evidence) for evidence in evidences]
        )
        print(
            "[INFO] Total evidences deleted: "
            f"{sum(results)} of {len(evidences)}"
        )
        print("[INFO] migration 0031 apply finished")


if __name__ == "__main__":
    execution_time = time.strftime(
        "Execution Time:    %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    run(main())
    finalization_time = time.strftime(
        "Finalization Time: %Y-%m-%d at %H:%M:%S UTC%Z"
    )
    print(f"{execution_time}\n{finalization_time}")
