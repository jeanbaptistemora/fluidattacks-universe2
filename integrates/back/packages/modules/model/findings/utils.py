
from typing import (
    List,
    Optional,
    cast,
)

from dynamodb.types import Item

from .enums import (
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from .types import (
    FindingState,
    FindingUnreliableIndicators,
    FindingVerification,
)


def format_state(state_item: Item) -> FindingState:
    return FindingState(
        modified_by=state_item['modified_by'],
        modified_date=state_item['modified_date'],
        source=state_item['source'],
        status=FindingStateStatus[state_item['status']],
    )


def format_state_item(state: FindingState) -> Item:
    return {
        'modified_by': state.modified_by,
        'modified_date': state.modified_date,
        'source': state.source,
        'status': state.status.value,
    }


def format_unreliable_indicators_item(
    indicators: FindingUnreliableIndicators
) -> Item:
    return {
        'unreliable_age': indicators.unreliable_age,
        'unreliable_closed_vulnerabilities': (
            indicators.unreliable_closed_vulnerabilities
        ),
        'unreliable_is_verified': indicators.unreliable_is_verified,
        'unreliable_last_vulnerability': (
            indicators.unreliable_last_vulnerability
        ),
        'unreliable_open_age': indicators.unreliable_open_age,
        'unreliable_open_vulnerabilities': (
            indicators.unreliable_open_vulnerabilities
        ),
        'unreliable_report_date': indicators.unreliable_report_date,
        'unreliable_status': indicators.unreliable_status.value,
    }


def format_unreliable_indicators(
    indicators_item: Item
) -> FindingUnreliableIndicators:
    return FindingUnreliableIndicators(
        unreliable_age=indicators_item['unreliable_age'],
        unreliable_closed_vulnerabilities=(
            indicators_item['unreliable_closed_vulnerabilities']
        ),
        unreliable_is_verified=indicators_item['unreliable_is_verified'],
        unreliable_last_vulnerability=(
            indicators_item['unreliable_last_vulnerability']
        ),
        unreliable_open_age=indicators_item['unreliable_open_age'],
        unreliable_open_vulnerabilities=(
            indicators_item['unreliable_open_vulnerabilities']
        ),
        unreliable_report_date=indicators_item['unreliable_report_date'],
        unreliable_status=FindingStatus[indicators_item['unreliable_status']],
    )


def format_verification(
    verification_item: Item
) -> Optional[FindingVerification]:
    verification = None
    if verification_item.get('status'):
        verification = FindingVerification(
            comment_id=verification_item['comment_id'],
            modified_by=verification_item['modified_by'],
            modified_date=verification_item['modified_date'],
            status=FindingVerificationStatus[verification_item['status']],
            vuln_uuids=tuple(cast(List[str], verification_item['vuln_uuids'])),
        )
    return verification


def format_verification_item(
    verification: Optional[FindingVerification]
) -> Item:
    verification_item = {}
    if verification is not None:
        verification_item = {
            'comment_id': verification.comment_id,
            'modified_by': verification.modified_by,
            'modified_date': verification.modified_date,
            'status': verification.status.value,
            'vuln_uuids': list(verification.vuln_uuids)
        }
    return verification_item
