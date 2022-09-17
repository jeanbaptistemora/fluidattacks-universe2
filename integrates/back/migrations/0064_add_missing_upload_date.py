# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0
# type: ignore

# pylint: disable=invalid-name,import-error
"""
This migration aims to add upload_date when missing,
taking it from LastModified

Execution Time: 2021-01-26 21:41:08 UTC-5
Finalization Time: 2021-01-26 21:51:47 UTC-5
"""

from aioextensions import (
    collect,
    run,
)
from context import (
    FI_AWS_S3_BUCKET,
)
from custom_types import (  # pylint: disable=import-error
    Finding,
)
from dataloaders.group import (
    GroupLoader,
)
from findings import (
    dal as findings_dal,
)
from groups.domain import (
    get_active_groups,
)
from itertools import (
    chain,
)
from more_itertools import (
    chunked,
)
from newutils import (
    datetime as datetime_utils,
)
import os
from s3.resource import (
    get_s3_resource,
)
from typing import (
    Dict,
    List,
)

STAGE: str = os.environ["STAGE"]


async def add_missing_upload_date(finding: Dict[str, Finding]) -> None:
    finding_id = str(finding["finding_id"])
    group_name = str(finding["project_name"])
    key_list = []
    date_list = []
    coroutines = []
    finding_prefix = f"{group_name}/{finding_id}/"
    client = await get_s3_resource()
    resp = await client.list_objects_v2(
        Bucket=FI_AWS_S3_BUCKET, Prefix=finding_prefix
    )
    key_list = [item["Key"] for item in resp.get("Contents", [])]
    date_list = [item["LastModified"] for item in resp.get("Contents", [])]

    for index, evidence in enumerate(finding.get("files", [])):
        if "upload_date" not in evidence and evidence.get("file_url"):
            file_url = finding_prefix + evidence["file_url"]
            if file_url in key_list:
                file_index = key_list.index(file_url)
                unaware_datetime = date_list[file_index]
                upload_date = datetime_utils.get_as_str(unaware_datetime)
                coroutines.append(
                    findings_dal.update(
                        finding_id,
                        {f"files[{index}].upload_date": upload_date},
                    )
                )

    if len(coroutines) > 0:
        if STAGE == "apply":
            await collect(coroutines)
        else:
            print(f"should update finding {finding_id}")


async def get_groups_findings(groups: List[str]) -> None:
    groups_data = await GroupLoader().load_many(groups)
    findings_ids = list(
        chain.from_iterable(
            group_data["findings"] + group_data["drafts"]
            for group_data in groups_data
        )
    )
    findings = await collect(map(findings_dal.get_finding, findings_ids))

    await collect(map(add_missing_upload_date, findings), workers=10)


async def main() -> None:
    groups = await get_active_groups()
    await collect(
        [get_groups_findings(list_group) for list_group in chunked(groups, 5)],
        workers=10,
    )


if __name__ == "__main__":
    run(main())
