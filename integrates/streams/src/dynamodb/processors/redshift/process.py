from . import (
    events as events_ops,
    findings as findings_ops,
    groups as groups_ops,
    organizations as orgs_ops,
    roots as roots_ops,
    toe_inputs as toe_inputs_ops,
    toe_lines as toe_lines_ops,
    vulnerabilities as vulns_ops,
)
from .operations import (
    db_cursor,
)
from collections.abc import (
    Iterator,
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


def _process_events(cursor: cursor_cls, records: tuple[Record, ...]) -> None:
    metadata_items: list[Item] = [
        record.old_image for record in records if record.old_image
    ]
    for item in metadata_items:
        events_ops.insert_metadata(cursor=cursor, item=item)
        LOGGER.info(
            "Event metadata stored, group: %s, id: %s",
            item["sk"].split("#")[1],
            item["pk"].split("#")[1],
        )


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


def _process_findings(cursor: cursor_cls, records: tuple[Record, ...]) -> None:
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


def _process_group_metadata(cursor: cursor_cls, item: Item) -> None:
    groups_ops.insert_group(cursor=cursor, item=item)
    LOGGER.info(
        "Group metadata stored, org: %s, id: %s",
        item["name"],
        item["organization_id"],
    )


def _process_groups(cursor: cursor_cls, records: tuple[Record, ...]) -> None:
    metadata_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith("ORG#")
    ]
    for item in metadata_items:
        _process_group_metadata(cursor, item)

    for key, items in _get_items_iterator(records, "STATE#"):
        group_name = str(key).split("#")[1]
        groups_ops.insert_historic_state(
            cursor=cursor, group_name=group_name, historic_state=tuple(items)
        )

    indicators_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.endswith("#UNRELIABLEINDICATORS")
    ]
    for item in indicators_items:
        groups_ops.insert_code_languages(
            cursor=cursor, unreliable_indicators=item
        )


def _process_organization_metadata(cursor: cursor_cls, item: Item) -> None:
    orgs_ops.insert_organization(cursor=cursor, item=item)
    LOGGER.info(
        "Organization metadata stored, id: %s, name: %s",
        item["id"],
        item["name"],
    )


def _process_organizations(
    cursor: cursor_cls, records: tuple[Record, ...]
) -> None:
    metadata_items: list[Item] = [
        record.old_image
        for record in records
        if record.old_image and record.sk.startswith("ORG#")
    ]
    for item in metadata_items:
        _process_organization_metadata(cursor, item)

    for key, items in _get_items_iterator(records, "STATE#"):
        organization_id = str(key).split("#")[1]
        orgs_ops.insert_historic_state(
            cursor=cursor,
            historic_state=tuple(items),
            organization_id=organization_id,
        )


def _process_roots(cursor: cursor_cls, records: tuple[Record, ...]) -> None:
    metadata_items: list[Item] = [
        record.old_image for record in records if record.old_image
    ]
    for item in metadata_items:
        roots_ops.insert_root(cursor=cursor, item=item)
        LOGGER.info(
            "Root metadata stored, group: %s, id: %s",
            item["sk"].split("#")[1],
            item["pk"].split("#")[1],
        )


def _process_toe_inputs(
    cursor: cursor_cls, records: tuple[Record, ...]
) -> None:
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


def _process_toe_lines(
    cursor: cursor_cls, records: tuple[Record, ...]
) -> None:
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


def _process_vulnerabilities(
    cursor: cursor_cls, records: tuple[Record, ...]
) -> None:
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


def process_records(records: tuple[Record, ...]) -> None:
    with db_cursor() as cursor:
        _process_events(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("EVENT#")
                    and record.sk.startswith("GROUP#"),
                    records,
                )
            ),
        )
        _process_findings(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("FIN#"),
                    records,
                )
            ),
        )
        _process_groups(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("GROUP#")
                    and (
                        record.sk.startswith("GROUP#")
                        or record.sk.startswith("ORG#")
                        or record.sk.startswith("STATE#")
                    ),
                    records,
                )
            ),
        )
        _process_organizations(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("ORG#")
                    and (
                        record.sk.startswith("ORG#")
                        or record.sk.startswith("STATE#")
                    ),
                    records,
                )
            ),
        )
        _process_roots(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("ROOT#")
                    and record.sk.startswith("GROUP#"),
                    records,
                )
            ),
        )
        _process_toe_inputs(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("GROUP#")
                    and record.sk.startswith("INPUTS#"),
                    records,
                )
            ),
        )
        _process_toe_lines(
            cursor=cursor,
            records=tuple(
                filter(
                    lambda record: record.pk.startswith("GROUP#")
                    and record.sk.startswith("LINES#"),
                    records,
                )
            ),
        )
        _process_vulnerabilities(
            cursor=cursor,
            records=tuple(
                filter(lambda record: record.pk.startswith("VULN#"), records)
            ),
        )
