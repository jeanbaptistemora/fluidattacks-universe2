from .types import (
    FindingVulnerabilitiesRequest,
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from .utils import (
    filter_non_deleted,
    filter_released_and_non_zero_risk,
    filter_released_and_zero_risk,
    format_state,
    format_treatment,
    format_verification,
    format_vulnerability,
    format_vulnerability_edge,
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
    RequiredStateStatus,
    VulnNotFound,
)
from db_model import (
    TABLE,
)
from db_model.vulnerabilities.constants import (
    ASSIGNED_INDEX_METADATA,
    EVENT_INDEX_METADATA,
    NEW_ZR_INDEX_METADATA,
    ROOT_INDEX_METADATA,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityVerificationStatus,
)
from dynamodb import (
    conditions,
    keys,
    operations,
)
from itertools import (
    chain,
)
from typing import (
    Any,
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
        limit=1,
        table=TABLE,
    )

    if not response.items:
        raise VulnNotFound()

    return format_vulnerability(response.items[0])


async def _get_historic_state(
    *,
    vulnerability_id: str,
) -> tuple[VulnerabilityState, ...]:
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
) -> tuple[VulnerabilityTreatment, ...]:
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
) -> tuple[VulnerabilityVerification, ...]:
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
) -> tuple[VulnerabilityZeroRisk, ...]:
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
) -> list[Vulnerability]:
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

    return list(format_vulnerability(item) for item in response.items)


async def _get_finding_vulnerabilities_released_zr(
    is_released: bool,
    is_zero_risk: bool,
    request: FindingVulnerabilitiesZrRequest,
) -> VulnerabilitiesConnection:
    gsi_6_index = TABLE.indexes["gsi_6"]
    key_values = {
        "finding_id": request.finding_id,
        "is_deleted": "false",
        "is_released": str(is_released).lower(),
        "is_zero_risk": str(is_zero_risk).lower(),
    }
    if isinstance(request.state_status, VulnerabilityStateStatus):
        key_values["state_status"] = str(request.state_status.value).lower()
    if isinstance(
        request.verification_status, VulnerabilityVerificationStatus
    ):
        if request.state_status is None:
            raise RequiredStateStatus()
        key_values["verification_status"] = str(
            request.verification_status.value
        ).lower()
    primary_key = keys.build_key(
        facet=NEW_ZR_INDEX_METADATA,
        values=key_values,
    )

    key_structure = gsi_6_index.primary_key
    sort_key = (
        primary_key.sort_key
        if isinstance(
            request.verification_status, VulnerabilityVerificationStatus
        )
        else primary_key.sort_key.replace("#VERIF", "")
    )
    response = await operations.query(
        after=request.after,
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(sort_key)
        ),
        facets=(TABLE.facets["vulnerability_metadata"],),
        filter_expression=conditions.get_filter_expression(
            request.filters._asdict()
        ),
        index=gsi_6_index,
        limit=request.first,
        paginate=request.paginate,
        table=TABLE,
    )

    return VulnerabilitiesConnection(
        edges=tuple(
            format_vulnerability_edge(gsi_6_index, item, TABLE)
            for item in response.items
        ),
        page_info=response.page_info,
    )


async def _get_root_vulnerabilities(
    *, root_id: str
) -> tuple[Vulnerability, ...]:
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


async def _get_assigned_vulnerabilities(*, email: str) -> list[Vulnerability]:
    primary_key = keys.build_key(
        facet=ASSIGNED_INDEX_METADATA,
        values={"email": email},
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

    return list(format_vulnerability(item) for item in response.items)


async def _get_affected_reattacks(
    *, event_id: str
) -> tuple[Vulnerability, ...]:
    primary_key = keys.build_key(
        facet=EVENT_INDEX_METADATA,
        values={"event_id": event_id},
    )

    index = TABLE.indexes["gsi_4"]
    key_structure = index.primary_key
    response = await operations.query(
        condition_expression=(
            Key(key_structure.partition_key).eq(primary_key.partition_key)
            & Key(key_structure.sort_key).begins_with(primary_key.sort_key)
        ),
        facets=(EVENT_INDEX_METADATA,),
        table=TABLE,
        index=index,
    )

    return tuple(format_vulnerability(item) for item in response.items)


class AssignedVulnerabilitiesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, emails: list[str]
    ) -> list[list[Vulnerability]]:
        return list(
            await collect(
                tuple(
                    _get_assigned_vulnerabilities(email=email)
                    for email in emails
                )
            )
        )


class FindingVulnerabilitiesLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    def clear(self, key: str) -> Any:
        self.dataloader.clear(key)
        return super().clear(key)

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: list[str]
    ) -> list[list[Vulnerability]]:
        vulns = list(
            await collect(
                tuple(
                    _get_finding_vulnerabilities(finding_id=finding_id)
                    for finding_id in finding_ids
                )
            )
        )
        for finding_vulns in vulns:
            for vuln in finding_vulns:
                self.dataloader.prime(vuln.id, vuln)
        return vulns


class FindingVulnerabilitiesDraftConnectionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: list[FindingVulnerabilitiesRequest]
    ) -> list[VulnerabilitiesConnection]:
        return list(
            await collect(
                tuple(
                    _get_finding_vulnerabilities_released_zr(
                        is_released=False,
                        is_zero_risk=False,
                        request=FindingVulnerabilitiesZrRequest(
                            finding_id=request.finding_id,
                            after=request.after,
                            first=request.first,
                            paginate=request.paginate,
                        ),
                    )
                    for request in requests
                )
            )
        )


class FindingVulnerabilitiesNonDeletedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    def clear(self, key: str) -> Any:
        self.dataloader.clear(key)
        return super().clear(key)

    async def load_many_chained(
        self, finding_ids: list[str]
    ) -> list[Vulnerability]:
        unchained_data = await self.load_many(finding_ids)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: list[str]
    ) -> list[list[Vulnerability]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return list(
            filter_non_deleted(finding_vulns)
            for finding_vulns in findings_vulns
        )


class FindingVulnerabilitiesReleasedNonZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    async def load_many_chained(
        self, finding_ids: list[str]
    ) -> list[Vulnerability]:
        unchained_data = await self.load_many(finding_ids)
        return list(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: list[str]
    ) -> list[list[Vulnerability]]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return list(
            filter_released_and_non_zero_risk(finding_vulns)
            for finding_vulns in findings_vulns
        )


class FindingVulnerabilitiesReleasedNonZeroRiskConnectionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: tuple[FindingVulnerabilitiesZrRequest, ...]
    ) -> tuple[VulnerabilitiesConnection, ...]:
        return await collect(
            tuple(
                _get_finding_vulnerabilities_released_zr(
                    is_released=True, is_zero_risk=False, request=request
                )
                for request in requests
            )
        )


class FindingVulnerabilitiesReleasedZeroRiskLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, finding_ids: list[str]
    ) -> tuple[tuple[Vulnerability, ...], ...]:
        findings_vulns = await self.dataloader.load_many(finding_ids)
        return tuple(
            filter_released_and_zero_risk(finding_vulns)
            for finding_vulns in findings_vulns
        )


class FindingVulnerabilitiesReleasedZeroRiskConnectionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: tuple[FindingVulnerabilitiesZrRequest, ...]
    ) -> tuple[VulnerabilitiesConnection, ...]:
        return await collect(
            tuple(
                _get_finding_vulnerabilities_released_zr(
                    is_released=True, is_zero_risk=True, request=request
                )
                for request in requests
            )
        )


class FindingVulnerabilitiesToReattackConnectionLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, requests: tuple[FindingVulnerabilitiesRequest, ...]
    ) -> tuple[VulnerabilitiesConnection, ...]:
        return await collect(
            tuple(
                _get_finding_vulnerabilities_released_zr(
                    is_released=True,
                    is_zero_risk=False,
                    request=FindingVulnerabilitiesZrRequest(
                        finding_id=request.finding_id,
                        after=request.after,
                        first=request.first,
                        paginate=request.paginate,
                        state_status=VulnerabilityStateStatus.VULNERABLE,
                        verification_status=(
                            VulnerabilityVerificationStatus.REQUESTED
                        ),
                    ),
                )
                for request in requests
            )
        )


class RootVulnerabilitiesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[Vulnerability, ...], ...]:
        return await collect(
            _get_root_vulnerabilities(root_id=id) for id in ids
        )


class EventVulnerabilitiesLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[Vulnerability, ...], ...]:
        return await collect(
            _get_affected_reattacks(event_id=id) for id in ids
        )


class VulnerabilityLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[Vulnerability, ...]:
        return await collect(
            tuple(_get_vulnerability(vulnerability_id=id) for id in ids)
        )


class VulnerabilityHistoricStateLoader(DataLoader):
    async def load_many_chained(
        self, ids: list[str]
    ) -> tuple[VulnerabilityState, ...]:
        unchained_data = await self.load_many(ids)
        return tuple(chain.from_iterable(unchained_data))

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[VulnerabilityState, ...], ...]:
        return await collect(
            tuple(_get_historic_state(vulnerability_id=id) for id in ids)
        )


class VulnerabilityHistoricTreatmentLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[VulnerabilityTreatment, ...], ...]:
        return await collect(
            tuple(_get_historic_treatment(vulnerability_id=id) for id in ids),
            workers=32,
        )


class VulnerabilityHistoricVerificationLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[VulnerabilityVerification, ...], ...]:
        return await collect(
            tuple(
                _get_historic_verification(vulnerability_id=id) for id in ids
            ),
            workers=32,
        )


class VulnerabilityHistoricZeroRiskLoader(DataLoader):
    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, ids: tuple[str, ...]
    ) -> tuple[tuple[VulnerabilityZeroRisk, ...], ...]:
        return await collect(
            tuple(_get_historic_zero_risk(vulnerability_id=id) for id in ids)
        )
