from botocore.exceptions import (
    ClientError,
)
from collections import (
    defaultdict,
)
from context import (
    FI_AWS_S3_MAIN_BUCKET,
    FI_AWS_S3_PATH_PREFIX,
)
from contextlib import (
    suppress,
)
import csv
from custom_exceptions import (
    UnavailabilityError,
    UnsanitizedInputFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLinesConnection,
)
import logging
import logging.config
from newutils.datetime import (
    get_as_str,
    get_now,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)
import os
from s3.operations import (
    sign_url,
)
from s3.resource import (
    get_s3_resource,
)
from settings.logger import (
    LOGGING,
)
import tempfile

logging.config.dictConfig(LOGGING)

LOGGER = logging.getLogger(__name__)


async def upload_file(bucket: str, file_path: str, file_name: str) -> None:
    with open(file_path, mode="rb") as file_object:
        client = await get_s3_resource()
        try:
            await client.upload_fileobj(
                file_object,
                bucket,
                file_name.lstrip("/"),
            )
        except ClientError as ex:
            LOGGER.exception(ex, extra={"extra": locals()})
            raise UnavailabilityError() from ex


def _get_valid_field(field: str) -> str:
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(field)
        return field
    return ""


async def get_group_toe_lines_report_url(
    *,
    loaders: Dataloaders,
    group_name: str,
) -> str:
    rows: list[list[str]] = [
        [
            "bePresent",
            "filename",
            "hasVulnerabilities",
            "lastAuthor",
            "lastCommit",
            "loc",
            "rootId",
            "rootNickname",
        ]
    ]
    group_toe_lines: ToeLinesConnection = await loaders.group_toe_lines.load(
        GroupToeLinesRequest(group_name=group_name)
    )
    group_roots = await loaders.group_roots.load(group_name)
    root_nickname_by_id: defaultdict[str, str] = defaultdict(str)

    for root in group_roots:
        root_nickname_by_id[root.id.lower()] = root.state.nickname

    for toe_line in group_toe_lines.edges:
        rows.append(
            [
                str(toe_line.node.state.be_present),
                _get_valid_field(toe_line.node.filename),
                str(toe_line.node.state.has_vulnerabilities),
                _get_valid_field(toe_line.node.state.last_author),
                _get_valid_field(toe_line.node.state.last_commit),
                str(toe_line.node.state.loc),
                toe_line.node.root_id,
                _get_valid_field(
                    root_nickname_by_id[toe_line.node.root_id.lower()]
                ),
            ]
        )

    date: str = get_as_str(get_now(), date_format="%Y-%m-%dT%H-%M-%S")
    csv_filename = f"{group_name}-{date}.csv"
    with tempfile.TemporaryDirectory() as directory:
        with open(
            os.path.join(directory, csv_filename),
            mode="w",
            encoding="utf-8",
        ) as csv_file:
            writer = csv.writer(
                csv_file,
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )
            writer.writerow(rows[0])
            writer.writerows(rows[1:])

        await upload_file(
            FI_AWS_S3_MAIN_BUCKET,
            str(csv_file.name),
            f"{FI_AWS_S3_PATH_PREFIX}reports/toe_lines/{csv_filename}",
        )

        return await sign_url(
            f"reports/toe_lines/{csv_filename}",
            600,
        )
