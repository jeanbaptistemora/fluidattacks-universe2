from .types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from .utils import (
    format_state,
    format_treatment,
    format_verification,
    format_vulnerability,
    format_zero_risk,
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
from typing import (
    Tuple,
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
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
    )
    if not results:
        raise VulnNotFound()
    inverted_index = TABLE.indexes["inverted_index"]
    inverted_key_structure = inverted_index.primary_key
    metadata = historics.get_metadata(
        item_id=primary_key.partition_key,
        key_structure=inverted_key_structure,
        raw_items=results,
    )

    return metadata[inverted_key_structure.partition_key].split("#")[1]


async def _get_vulnerability(*, uuid: str) -> Vulnerability:
    finding_id = await _get_finding(uuid=uuid)

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

    return format_vulnerability(
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


async def _get_historic_verification(
    *, uuid: str
) -> Tuple[VulnerabilityVerification, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_verification"],
        values={"uuid": uuid},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_verification"],),
        table=TABLE,
    )
    return tuple(map(format_verification, results))


async def _get_historic_zero_risk(
    *, uuid: str
) -> Tuple[VulnerabilityZeroRisk, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_zero_risk"],
        values={"uuid": uuid},
    )
    key_structure = TABLE.primary_key
    results = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_zero_risk"],),
        table=TABLE,
    )
    return tuple(map(format_zero_risk, results))


class VulnNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(_get_vulnerability(uuid=uuid) for uuid in uuids)


class VulnHistoricStateNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityState], ...]:
        return await collect(_get_historic_state(uuid=uuid) for uuid in uuids)


class VulnHistoricTreatmentNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityTreatment], ...]:
        return await collect(
            _get_historic_treatment(uuid=uuid) for uuid in uuids
        )


class VulnHistoricVerificationNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityVerification], ...]:
        return await collect(
            _get_historic_verification(uuid=uuid) for uuid in uuids
        )


class VulnHistoricZeroRiskNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, uuids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityZeroRisk], ...]:
        return await collect(
            _get_historic_zero_risk(uuid=uuid) for uuid in uuids
        )
