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
    keys,
    operations,
)
from typing import (
    Tuple,
)


async def _get_vulnerability(*, vulnerability_id: str) -> Vulnerability:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"id": vulnerability_id},
    )

    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
    )

    if not response.items:
        raise VulnNotFound()

    return format_vulnerability(response.items[0])


async def _get_historic_state(
    *,
    vulnerability_id: str,
) -> Tuple[VulnerabilityState, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_state"],
        values={"id": vulnerability_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_state"],),
        table=TABLE,
    )
    return tuple(map(format_state, response.items))


async def _get_historic_treatment(
    *,
    vulnerability_id: str,
) -> Tuple[VulnerabilityTreatment, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_treatment"],
        values={"id": vulnerability_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_treatment"],),
        table=TABLE,
    )
    return tuple(map(format_treatment, response.items))


async def _get_historic_verification(
    *,
    vulnerability_id: str,
) -> Tuple[VulnerabilityVerification, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_verification"],
        values={"id": vulnerability_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_verification"],),
        table=TABLE,
    )
    return tuple(map(format_verification, response.items))


async def _get_historic_zero_risk(
    *,
    vulnerability_id: str,
) -> Tuple[VulnerabilityZeroRisk, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_historic_zero_risk"],
        values={"id": vulnerability_id},
    )
    key_structure = TABLE.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(TABLE.facets["vulnerability_historic_zero_risk"],),
        table=TABLE,
    )
    return tuple(map(format_zero_risk, response.items))


class VulnNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(
            _get_vulnerability(vulnerability_id=id) for id in ids
        )


class VulnHistoricStateNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityState, ...], ...]:
        return await collect(
            _get_historic_state(vulnerability_id=id) for id in ids
        )


class VulnHistoricTreatmentNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityTreatment, ...], ...]:
        return await collect(
            _get_historic_treatment(vulnerability_id=id) for id in ids
        )


class VulnHistoricVerificationNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityVerification, ...], ...]:
        return await collect(
            _get_historic_verification(vulnerability_id=id) for id in ids
        )


class VulnHistoricZeroRiskNewLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityZeroRisk, ...], ...]:
        return await collect(
            _get_historic_zero_risk(vulnerability_id=id) for id in ids
        )
