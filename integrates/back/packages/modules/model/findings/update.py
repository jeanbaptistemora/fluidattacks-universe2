
from enum import Enum

from boto3.dynamodb.conditions import Attr

from dynamodb import (
    historics,
    keys,
    operations,
)
from model import TABLE

from .enums import FindingStateStatus
from .types import (
    FindingUnreliableIndicatorsToUpdate,
    FindingState,
    FindingVerification,
)
from .utils import (
    format_state_item,
    format_verification_item,
)


async def update_state(
    *,
    group_name: str,
    finding_id: str,
    state: FindingState
) -> None:
    items = []
    key_structure = TABLE.primary_key
    state_item = format_state_item(state)
    latest, historic = historics.build_historic(
        attributes=state_item,
        historic_facet=TABLE.facets['finding_historic_state'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': state.modified_date,
            'group_name': group_name,
            'id': finding_id
        },
        latest_facet=TABLE.facets['finding_state'],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=TABLE.facets['finding_state'],
        item=latest,
        table=TABLE
    )
    items.append(historic)
    if state.status == FindingStateStatus.APPROVED:
        approval_key = keys.build_key(
            facet=TABLE.facets['finding_approval'],
            values={'group_name': group_name, 'id': finding_id},
        )
        approval = {
            key_structure.partition_key: approval_key.partition_key,
            key_structure.sort_key: approval_key.sort_key,
            **state_item
        }
        items.append(approval)
    elif state.status == FindingStateStatus.SUBMITTED:
        submission_key = keys.build_key(
            facet=TABLE.facets['finding_submission'],
            values={'group_name': group_name, 'id': finding_id},
        )
        submission = {
            key_structure.partition_key: submission_key.partition_key,
            key_structure.sort_key: submission_key.sort_key,
            **state_item
        }
        items.append(submission)
    await operations.batch_write_item(items=tuple(items), table=TABLE)


async def update_unreliable_indicators(
    *,
    group_name: str,
    finding_id: str,
    indicators: FindingUnreliableIndicatorsToUpdate,
) -> None:
    key_structure = TABLE.primary_key
    unreliable_indicators_key = keys.build_key(
        facet=TABLE.facets['finding_unreliable_indicators'],
        values={'group_name': group_name, 'id': finding_id}
    )
    unreliable_indicators = {
        key: value.value if isinstance(value, Enum) else value
        for key, value in indicators._asdict().items()
        if value is not None
    }
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.update_item(
        condition_expression=condition_expression,
        item=unreliable_indicators,
        key=unreliable_indicators_key,
        table=TABLE
    )


async def update_verification(
    *,
    group_name: str,
    finding_id: str,
    verification: FindingVerification
) -> None:
    items = []
    key_structure = TABLE.primary_key
    verification_item = format_verification_item(verification)
    latest, historic = historics.build_historic(
        attributes=verification_item,
        historic_facet=TABLE.facets['finding_historic_verification'],
        key_structure=key_structure,
        key_values={
            'iso8601utc': verification.modified_date,
            'group_name': group_name,
            'id': finding_id
        },
        latest_facet=TABLE.facets['finding_verification'],
    )
    condition_expression = Attr(key_structure.partition_key).exists()
    await operations.put_item(
        condition_expression=condition_expression,
        facet=TABLE.facets['finding_verification'],
        item=latest,
        table=TABLE
    )
    items.append(historic)
    await operations.batch_write_item(items=tuple(items), table=TABLE)
