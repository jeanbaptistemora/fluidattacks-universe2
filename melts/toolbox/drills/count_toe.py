import boto3
from botocore.exceptions import (
    ClientError,
)
import csv
from datetime import (
    datetime,
)
import os
from toolbox.logger import (
    LOGGER,
)
from toolbox.utils.function import (
    shield,
)
from typing import (
    Any,
    Tuple,
)


def get_dynamodb_resource() -> Any:
    return boto3.resource(
        "dynamodb",
        aws_access_key_id=os.environ["AWS_ACCESS_KEY_ID"],
        aws_secret_access_key=os.environ["AWS_SECRET_ACCESS_KEY"],
        region_name=os.environ["AWS_DEFAULT_REGION"],
    )


def count_lines(file_csv: str) -> Tuple[int, int]:
    """Insert lines.csv"""
    with open(file_csv, encoding="utf8") as f_csv:
        reader = csv.reader(f_csv)
        next(reader, None)
        (lines, tested_lines) = (
            0,
            0,
        )
        for row in reader:
            if not row:
                continue

            if row[1] != "":
                lines += int(row[1])

            if len(row) > 2 and row[2] != "":
                tested_lines += int(row[2])

    return (lines, tested_lines)


def count_inputs(file_csv: str) -> Tuple[int, int]:
    """Insert campos.csv"""
    with open(file_csv, encoding="utf8") as f_csv:
        reader = csv.reader(f_csv)
        next(reader, None)
        (fields, tested_fields) = (0, 0)
        for row in reader:
            if row[1] != "":
                fields += 1

            if row[2] == "Yes":
                tested_fields += 1

    return (fields, tested_fields)


def insert_data(
    group: str,
    lines: int,
    tested_lines: int,
    fields: int,
    tested_fields: int,
) -> bool:
    """Insert data into table"""
    success: bool = True
    table = get_dynamodb_resource().Table("FI_toe")
    try:
        response = table.put_item(
            Item={
                "project": group,
                "lines": lines,
                "lines_tested": tested_lines,
                "fields": fields,
                "fields_tested": tested_fields,
                "last_update": str(datetime.now().date()),
            }
        )
        success = response["ResponseMetadata"]["HTTPStatusCode"] == 200
    except ClientError as exc:
        LOGGER.error("Could not insert data for %s", group)
        LOGGER.exception(exc)
        success = False
    else:
        LOGGER.info(
            "%s, %i lines, %i tested lines, %i inputs, %i tested inputs",
            group,
            lines,
            tested_lines,
            fields,
            tested_fields,
        )

    return success


@shield(on_error_return=False)
def main(target_group: str) -> bool:
    """main function"""
    success: bool = True

    groups = os.listdir("groups") if target_group == "all" else [target_group]

    for group in sorted(groups):
        fields, tested_fields, lines, tested_lines = 0, 0, 0, 0

        inputs_file = os.path.join("groups", group, "toe/inputs.csv")
        lines_file = os.path.join("groups", group, "toe/lines.csv")

        if os.path.exists(inputs_file):
            fields, tested_fields = count_inputs(inputs_file)

        if os.path.exists(lines_file):
            lines, tested_lines = count_lines(lines_file)

        success = success and insert_data(
            group, lines, tested_lines, fields, tested_fields
        )

    return success
