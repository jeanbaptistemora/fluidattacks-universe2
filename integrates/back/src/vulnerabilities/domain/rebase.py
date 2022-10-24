# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
    InvalidVulnerabilityAlreadyExists,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
import logging
from settings.logger import (
    LOGGING,
)
from typing import (
    Tuple,
)
from vulnerabilities.domain.utils import (
    get_hash,
    get_path_from_integrates_vulnerability,
)
from vulnerabilities.domain.validations import (
    validate_commit_hash,
    validate_specific,
    validate_uniqueness,
    validate_where,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def rebase(
    *,
    finding_id: str,
    finding_vulns_data: Tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> None:
    if vulnerability_type != VulnerabilityType.LINES:
        raise ExpectedVulnToBeOfLinesType.new()

    validate_commit_hash(vulnerability_commit)
    validate_specific(vulnerability_specific)
    current_vuln: Vulnerability = next(
        vuln for vuln in finding_vulns_data if vuln.id == vulnerability_id
    )
    current_vuln_hash = get_hash(
        specific=current_vuln.specific,
        type_=current_vuln.type,
        where=get_path_from_integrates_vulnerability(
            current_vuln.where, current_vuln.type
        )[1]
        if current_vuln.type == VulnerabilityType.INPUTS
        else current_vuln.where,
        root_id=current_vuln.root_id,
    )
    for vuln in finding_vulns_data:
        vuln_hash: int = get_hash(
            specific=vuln.specific,
            type_=vuln.type,
            where=get_path_from_integrates_vulnerability(
                vuln.where, vuln.type
            )[1]
            if vuln.type == VulnerabilityType.INPUTS
            else vuln.where,
            root_id=vuln.root_id,
        )
        if vuln_hash == current_vuln_hash and vuln.id != current_vuln.id:
            LOGGER.warning(
                "there is a problem with the rebase vulnerability",
                extra={
                    "extra": {
                        "vuln_to_rebase": {
                            "id": current_vuln.id,
                            "path": current_vuln.where,
                            "line": current_vuln.specific,
                            "root_id": current_vuln.root_id,
                        },
                        "vuln_overwrite": {
                            "id": vuln.id,
                            "path": vuln.where,
                            "line": vuln.specific,
                            "root_id": vuln.root_id,
                        },
                    }
                },
            )

    try:
        validate_uniqueness(
            finding_vulns_data=finding_vulns_data,
            vulnerability_where=vulnerability_where,
            vulnerability_specific=vulnerability_specific,
            vulnerability_type=vulnerability_type,
            vulnerability_id=vulnerability_id,
        )
    except InvalidVulnerabilityAlreadyExists as exc:
        for vuln in finding_vulns_data:
            if (
                vuln.id == vulnerability_id
                and vuln.commit == vulnerability_commit
            ):
                raise exc

    validate_where(vulnerability_where)

    await vulns_model.update_metadata(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        metadata=VulnerabilityMetadataToUpdate(
            commit=vulnerability_commit,
            specific=vulnerability_specific,
            where=vulnerability_where,
        ),
    )
