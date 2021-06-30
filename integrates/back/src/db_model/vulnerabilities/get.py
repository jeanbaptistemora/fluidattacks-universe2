from .historics.state import (
    format_state,
    VulnerabilityState,
)
from .historics.treatment import (
    format_treatment,
    VulnerabilityTreatment,
)
from .historics.verification import (
    format_verification,
    VulnerabilityVerification,
)
from .historics.zero_risk import (
    format_zero_risk,
    VulnerabilityZeroRisk,
)
from .metadata import (
    Vulnerability,
)
from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from custom_exceptions import (
    VulnNotFound,
)
from db_model import (
    TABLE,
)
from dynamodb import (
    historics,
    keys,
    operations,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)
from typing import (
    Optional,
    Tuple,
)


def _build_vulnerability(
    *,
    item_id: str,
    key_structure: PrimaryKey,
    raw_items: Tuple[Item, ...],
) -> Vulnerability:
    metadata = historics.get_metadata(
        item_id=item_id, key_structure=key_structure, raw_items=raw_items
    )
    state: VulnerabilityState = format_state(
        historics.get_latest(
            item_id=item_id,
            key_structure=key_structure,
            historic_suffix="STATE",
            raw_items=raw_items,
        )
    )

    try:
        treatment: Optional[VulnerabilityTreatment] = format_treatment(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="TREAT",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        treatment = None

    try:
        verification: Optional[
            VulnerabilityVerification
        ] = format_verification(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="VERIF",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        verification = None

    try:
        zero_risk: Optional[VulnerabilityZeroRisk] = format_zero_risk(
            historics.get_latest(
                item_id=item_id,
                key_structure=key_structure,
                historic_suffix="ZERO",
                raw_items=raw_items,
            )
        )
    except StopIteration:
        zero_risk = None

    return Vulnerability(
        bts_url=metadata.get("bts_url", None),
        commit=metadata.get("commit", None),
        custom_severity=metadata.get("custom_severity", None),
        finding_id=metadata["finding_id"],
        hash=metadata.get("hash", None),
        repo=metadata.get("bts_url", None),
        specific=metadata["specific"],
        state=state,
        stream=metadata.get("stream", None),
        uuid=metadata["uuid"],
        tags=metadata.get("tags", None),
        treatment=treatment,
        type=metadata["type"],
        verification=verification,
        where=metadata["where"],
        zero_risk=zero_risk,
    )


async def _get_finding(*, uuid: str) -> str:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"uuid": uuid},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["finding_metadata"],),
        table=TABLE,
    )

    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=results,
    )

    if not results:
        raise VulnNotFound()

    return metadata[inverted_key_structure.partition_key].split("#")[1]


async def _get_vulnerability(*, uuid: str) -> Vulnerability:
    finding_id = _get_finding(uuid=uuid)

    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id, "uuid": uuid},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(
            TABLE.facets["vulnerability_metadata"],
            TABLE.facets["vulnerability_state"],
            TABLE.facets["vulnerability_treatment"],
            TABLE.facets["vulnerability_verification"],
            TABLE.facets["vulnerability_zero_risk"],
        ),
        index=index,
        table=TABLE,
    )

    if not results:
        raise VulnNotFound()

    return _build_vulnerability(
        item_id=primary_key.partition_key,
        key_structure=key_structure,
        raw_items=results,
    )


async def _get_historic_state(*, uuid: str) -> Tuple[VulnerabilityState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={"uuid": uuid},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_state"],),
        table=TABLE,
    )
    return tuple(map(format_state, results))


async def _get_historic_treatment(
    *, uuid: str
) -> Tuple[VulnerabilityTreatment, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        values={"uuid": uuid},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_treatment"],),
        table=TABLE,
    )
    return tuple(map(format_treatment, results))


class VulnerabilityNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(_get_vulnerability(uuid=uuid) for uuid in uuids)


class VulnerabilityHistoricStateNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityState], ...]:
        return await collect(_get_historic_state(uuid=uuid) for uuid in uuids)


class VulnerabilityHistoricTreatmentNewLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityTreatment], ...]:
        return await collect(
            _get_historic_treatment(uuid=uuid) for uuid in uuids
        )
