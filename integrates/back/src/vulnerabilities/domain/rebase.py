from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
    InvalidVulnerabilityAlreadyExists,
)
from dataloaders import (
    Dataloaders,
)
from db_model import (
    vulnerabilities as vulns_model,
)
from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
)
import logging
from newutils import (
    datetime as datetime_utils,
)
from newutils.vulnerabilities import (
    validate_vulnerability_in_toe,
)
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
    validate_lines_specific,
    validate_uniqueness,
    validate_where,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


async def rebase(
    *,
    loaders: Dataloaders,
    finding_id: str,
    finding_vulns_data: Tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> VulnerabilityState:
    if vulnerability_type != VulnerabilityType.LINES:
        raise ExpectedVulnToBeOfLinesType.new()

    validate_commit_hash(vulnerability_commit)
    validate_lines_specific(vulnerability_specific)
    current_vuln: Vulnerability = next(
        vuln for vuln in finding_vulns_data if vuln.id == vulnerability_id
    )
    await validate_vulnerability_in_toe(
        loaders,
        current_vuln.group_name,
        current_vuln._replace(
            state=current_vuln.state._replace(
                specific=vulnerability_specific,
                where=vulnerability_where,
                commit=vulnerability_commit,
            ),
        ),
        index=0,
    )
    current_vuln_hash = get_hash(
        specific=current_vuln.state.specific,
        type_=current_vuln.type,
        where=get_path_from_integrates_vulnerability(
            current_vuln.state.where, current_vuln.type
        )[1]
        if current_vuln.type == VulnerabilityType.INPUTS
        else current_vuln.state.where,
        root_id=current_vuln.root_id,
    )
    for vuln in finding_vulns_data:
        vuln_hash: int = get_hash(
            specific=vuln.state.specific,
            type_=vuln.type,
            where=get_path_from_integrates_vulnerability(
                vuln.state.where, vuln.type
            )[1]
            if vuln.type == VulnerabilityType.INPUTS
            else vuln.state.where,
            root_id=vuln.root_id,
        )
        if vuln_hash == current_vuln_hash and vuln.id != current_vuln.id:
            LOGGER.warning(
                "there is a problem with the rebase vulnerability",
                extra={
                    "extra": {
                        "vuln_to_rebase": {
                            "id": current_vuln.id,
                            "path": current_vuln.state.where,
                            "line": current_vuln.state.specific,
                            "root_id": current_vuln.root_id,
                        },
                        "vuln_overwrite": {
                            "id": vuln.id,
                            "path": vuln.state.where,
                            "line": vuln.state.specific,
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
                and vuln.state.commit == vulnerability_commit
            ):
                raise exc

    validate_where(vulnerability_where)
    vulns_states: Tuple[
        VulnerabilityState
    ] = await loaders.vulnerability_historic_state.load(vulnerability_id)
    last_state = vulns_states[-1]._replace(
        commit=vulnerability_commit,
        specific=vulnerability_specific,
        where=vulnerability_where,
        modified_date=datetime_utils.get_utc_now(),
        modified_by="rebase@fluidattacks.com",
        source=Source.ASM,
    )

    await vulns_model.update_historic_entry(
        current_value=current_vuln,
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        entry=last_state,
    )
    return last_state
