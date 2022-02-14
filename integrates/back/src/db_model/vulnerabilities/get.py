from .types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from .utils import (
    filter_non_deleted,
    filter_non_zero_risk,
    filter_zero_risk,
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
from db_model.vulnerabilities.constants import (
    ASSIGNED_INDEX_METADATA,
    ROOT_INDEX_METADATA,
)
from dynamodb import (
    keys,
    operations,
)
from itertools import (
    chain,
)
from typing import (
    List,
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


async def _get_finding_vulnerabilities(
    *, finding_id: str
) -> Tuple[Vulnerability, ...]:
    primary_key = keys.build_key(
        facet=TABLE.facets["vulnerability_metadata"],
        values={"finding_id": finding_id},
    )

    index = TABLE.indexes["inverted_index"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.sort_key)
            & Key(key_structure.sort_key).begins_with(
                primary_key.partition_key
            )
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        table=TABLE,
        index=index,
    )

    return tuple(format_vulnerability(item) for item in response.items)


async def _get_root_vulnerabilities(
    *, root_id: str
) -> Tuple[Vulnerability, ...]:
    primary_key = keys.build_key(
        facet=ROOT_INDEX_METADATA,
        values={"root_id": root_id},
    )

    index = TABLE.indexes["gsi_2"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ROOT_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    return tuple(format_vulnerability(item) for item in response.items)


async def _get_assigned_vulnerabilities(
    *, user_email: str
) -> Tuple[Vulnerability, ...]:
    primary_key = keys.build_key(
        facet=ASSIGNED_INDEX_METADATA,
        values={"email": user_email},
    )

    index = TABLE.indexes["gsi_3"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(ASSIGNED_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    return tuple(format_vulnerability(item) for item in response.items)


class AssignedVulnerabilitiesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, emails: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(
            tuple(
                _get_assigned_vulnerabilities(user_email=user_email)
                for user_email in emails
            )
        )


class FindingVulnerabilitiesLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        vulns = await collect(
            tuple(_get_finding_vulnerabilities(finding_id=id) for id in ids)
        )
        for finding_vulns in vulns:
            for vuln in finding_vulns:
                self.dataloader.prime(vuln.id, vuln)
        return vulns


class FindingVulnerabilitiesNonDeletedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    def clear(self, key: str) -> DataLoader:
        self.dataloader.clear(key)
        return super().clear(key)

    async def load_many_chained(
        self, finding_ids: List[str]
    ) -> Tuple[Vulnerability, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            filter_non_deleted(finding_vulns)
            for finding_vulns in findings_vulns
        )


class FindingVulnerabilitiesNonZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, finding_ids: List[str]
    ) -> Tuple[Vulnerability, ...]:
        unchained_data = await self.load_many(finding_ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            filter_non_zero_risk(finding_vulns)
            for finding_vulns in findings_vulns
        )


class FindingVulnerabilitiesOnlyZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: List[str]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            filter_zero_risk(finding_vulns) for finding_vulns in findings_vulns
        )


class RootVulnerabilitiesLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(
            _get_root_vulnerabilities(root_id=id) for id in ids
        )


class VulnerabilityLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Vulnerability, ...]:
        return await collect(
            tuple(_get_vulnerability(vulnerability_id=id) for id in ids)
        )


class VulnerabilityHistoricStateLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityState, ...], ...]:
        return await collect(
            tuple(_get_historic_state(vulnerability_id=id) for id in ids)
        )


class VulnerabilityHistoricTreatmentLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityTreatment, ...], ...]:
        return await collect(
            tuple(_get_historic_treatment(vulnerability_id=id) for id in ids)
        )


class VulnerabilityHistoricVerificationLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityVerification, ...], ...]:
        return await collect(
            tuple(
                _get_historic_verification(vulnerability_id=id) for id in ids
            )
        )


class VulnerabilityHistoricZeroRiskLoader(DataLoader):
    # pylint: disable=no-self-use,method-hidden
    async def batch_load_fn(
        self, ids: Tuple[str, ...]
    ) -> Tuple[Tuple[VulnerabilityZeroRisk, ...], ...]:
        return await collect(
            tuple(_get_historic_zero_risk(vulnerability_id=id) for id in ids)
        )
