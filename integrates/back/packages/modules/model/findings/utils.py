# Standard
from typing import cast, List

# Local
from dynamodb.types import Item
from .types import (
    FindingState,
    FindingVerification
)


def format_state(state_item: Item) -> FindingState:
    return FindingState(
        modified_by=state_item['modified_by'],
        modified_date=state_item['modified_date'],
        source=state_item['source'],
        status=state_item['status'],
    )


def format_state_item(state: FindingState) -> Item:
    return {
        'modified_by': state.modified_by,
        'modified_date': state.modified_date,
        'source': state.source,
        'status': state.status,
    }


def format_verification(verification_item: Item) -> FindingVerification:
    return FindingVerification(
        comment_id=verification_item['comment_id'],
        modified_by=verification_item['modified_by'],
        modified_date=verification_item['modified_date'],
        status=verification_item['status'],
        vuln_uuids=tuple(cast(List[str], verification_item['vuln_uuids'])),
    )


def format_verification_item(verification: FindingVerification) -> Item:
    return {
        **verification._asdict(),
        'vuln_uuids': list(verification.vuln_uuids)
    }
