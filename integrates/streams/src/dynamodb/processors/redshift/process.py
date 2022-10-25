# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0


from . import (
    findings as findings_ops,
    roots as roots_ops,
    toe_inputs as toe_inputs_ops,
    toe_lines as toe_lines_ops,
    vulnerabilities as vulns_ops,
)
from .operations import (
    db_cursor,
)
from dynamodb.types import (
    Item,
    Record,
)
import itertools
import logging
from operator import (
    itemgetter,
)
from psycopg2.extensions import (
    cursor as cursor_cls,
)
from typing import (
    Iterator,
)

FLUID_IDENTIFIER = "@fluidattacks.com"
LOGGER = logging.getLogger(__name__)


def _get_items_iterator(
    records: tuple[Record, ...], sk_prefix: str
) -> Iterator:
    filtered_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith(sk_prefix)
    ]

    return itertools.groupby(filtered_items, itemgetter("pk"))


def _process_finding_metadata(cursor: cursor_cls, item: Item) -> None:
    state: Item = item["state"]
    if state["status"] != "DELETED":
        findings_ops.insert_finding(cursor=cursor, item=item)
        LOGGER.info(
            "Finding metadata stored, group: %s, id: %s",
            item["group_name"],
            item["id"],
        )


def _process_finding_state(
    cursor: cursor_cls, finding_id: str, items: list[Item]
) -> None:
    findings_ops.insert_historic_state(
        cursor=cursor, finding_id=finding_id, historic_state=tuple(items)
    )


def _process_finding_verification(
    cursor: cursor_cls, finding_id: str, items: list[Item]
) -> None:
    findings_ops.insert_historic_verification(
        cursor=cursor,
        finding_id=finding_id,
        historic_verification=tuple(items),
    )
    findings_ops.insert_historic_verification_vuln_ids(
        cursor=cursor,
        finding_id=finding_id,
        historic_verification=tuple(items),
    )


def process_findings(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("GROUP#")
        ]
        for item in metadata_items:
            _process_finding_metadata(cursor, item)
        for key, items in _get_items_iterator(records, "STATE#"):
            finding_id = str(key).split("#")[1]
            _process_finding_state(cursor, finding_id, list(items))
        for key, items in _get_items_iterator(records, "VERIFICATION#"):
            finding_id = str(key).split("#")[1]
            _process_finding_verification(cursor, finding_id, list(items))


def process_roots(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("GROUP#")
        ]
        for item in metadata_items:
            roots_ops.insert_root(cursor=cursor, item=item)
            LOGGER.info(
                "Root metadata stored, group: %s, id: %s",
                item["sk"].split("#")[1],
                item["pk"].split("#")[1],
            )


def process_toe_inputs(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image for record in records if record.old_image
        ]
        for item in metadata_items:
            toe_inputs_ops.insert_metadata(cursor=cursor, item=item)
            LOGGER.info(
                "Toe inputs metadata stored, sk: %s, group: %s",
                item["sk"],
                item["group_name"],
            )


def process_toe_lines(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image for record in records if record.old_image
        ]
        for item in metadata_items:
            toe_lines_ops.insert_metadata(cursor=cursor, item=item)
            LOGGER.info(
                "Toe lines metadata stored, sk: %s, group: %s",
                item["sk"],
                item["group_name"],
            )


def _process_vulnerability_metadata(cursor: cursor_cls, item: Item) -> None:
    state: Item = item["state"]
    if state["status"] != "DELETED":
        vulns_ops.insert_vulnerability(cursor=cursor, item=item)
        LOGGER.info(
            "Vulnerability metadata stored, finding_id: %s, id: %s",
            item.get("finding_id") or str(item["sk"]).split("#")[1],
            item.get("id") or str(item["pk"]).split("#")[1],
        )


def process_vulnerabilities(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        metadata_items: list[Item] = [
            record.old_image
            for record in records
            if record.old_image and record.sk.startswith("FIN#")
        ]
        for item in metadata_items:
            _process_vulnerability_metadata(cursor, item)
        for key, items in _get_items_iterator(records, "STATE#"):
            vulns_ops.insert_historic_state(
                cursor=cursor,
                vulnerability_id=str(key).split("#")[1],
                historic_state=tuple(items),
            )
        for key, items in _get_items_iterator(records, "TREATMENT#"):
            vulns_ops.insert_historic_treatment(
                cursor=cursor,
                vulnerability_id=str(key).split("#")[1],
                historic_treatment=tuple(items),
            )
        for key, items in _get_items_iterator(records, "VERIFICATION#"):
            vulns_ops.insert_historic_verification(
                cursor=cursor,
                vulnerability_id=str(key).split("#")[1],
                historic_verification=tuple(items),
            )
        for key, items in _get_items_iterator(records, "ZERORISK#"):
            vulns_ops.insert_historic_zero_risk(
                cursor=cursor,
                vulnerability_id=str(key).split("#")[1],
                historic_zero_risk=tuple(items),
            )
