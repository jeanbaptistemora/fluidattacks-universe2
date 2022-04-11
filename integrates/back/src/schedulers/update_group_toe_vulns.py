from aioextensions import (
    collect,
)
from custom_exceptions import (
    ToeInputAlreadyUpdated,
    ToeLinesAlreadyUpdated,
)
from dataloaders import (
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.toe_inputs.types import (
    GroupToeInputsRequest,
    ToeInput,
)
from db_model.toe_lines.types import (
    GroupToeLinesRequest,
    ToeLines,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
from groups import (
    domain as groups_domain,
)
import logging
import logging.config
from newutils import (
    bugsnag as bugsnag_utils,
)
from settings import (
    LOGGING,
)
from toe.inputs import (
    domain as toe_inputs_domain,
)
from toe.inputs.types import (
    ToeInputAttributesToUpdate,
)
from toe.lines import (
    domain as toe_lines_domain,
)
from toe.lines.types import (
    ToeLinesAttributesToUpdate,
)
from typing import (
    Any,
    Dict,
    Tuple,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

bugsnag_utils.start_scheduler_session()


def _log(msg: str, **extra: Any) -> None:
    LOGGER.info(msg, extra={"extra": extra})


def _strip_first_dir(where: str) -> Tuple[str, str]:
    return (where[0 : where.find("/")], where[where.find("/") + 1 :])


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def update_toe_input(
    current_value: ToeInput, attributes: ToeInputAttributesToUpdate
) -> None:
    await toe_inputs_domain.update(
        current_value,
        attributes,
        is_moving_toe_input=True,
    )


@retry_on_exceptions(
    exceptions=(ToeInputAlreadyUpdated,),
)
async def process_toe_inputs(
    group_name: str, vulnerabilities: Tuple[Vulnerability, ...]
) -> None:
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    updations = []

    for toe_input in group_toe_inputs:
        has_vulnerabilities: bool = any(
            vulnerability.state.status is VulnerabilityStateStatus.OPEN
            # ToeInput is not associated to a root_id
            # and vulnerability.root_id == toe_input.root_id
            and vulnerability.where == toe_input.component
            and vulnerability.specific == toe_input.entry_point
            for vulnerability in vulnerabilities
        )

        if toe_input.has_vulnerabilities != has_vulnerabilities:
            updations.append(
                update_toe_input(
                    toe_input,
                    ToeInputAttributesToUpdate(
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
            )

    await collect(tuple(updations))


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def update_toe_lines(
    current_value: ToeLines, attributes: ToeLinesAttributesToUpdate
) -> None:
    await toe_lines_domain.update(
        current_value,
        attributes,
        is_moving_toe_lines=True,
    )


@retry_on_exceptions(
    exceptions=(ToeLinesAlreadyUpdated,),
)
async def process_toe_lines(
    group_name: str,
    vulnerabilities: Tuple[Vulnerability, ...],
    root_nicknames: Dict[str, str],
) -> None:
    loaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name)
    )

    updations = []

    for toe_line in group_toe_lines:
        has_vulnerabilities = any(
            vulnerability.state.status is VulnerabilityStateStatus.OPEN
            and vulnerability_where_repo == root_nicknames[toe_line.root_id]
            and vulnerability_where_path.startswith(toe_line.filename)
            for vulnerability in vulnerabilities
            for vulnerability_where_repo, vulnerability_where_path in [
                _strip_first_dir(vulnerability.where)
            ]
        )

        if toe_line.has_vulnerabilities != has_vulnerabilities:
            updations.append(
                update_toe_lines(
                    toe_line,
                    ToeLinesAttributesToUpdate(
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
            )

    await collect(tuple(updations))


async def process_group(group_name: str) -> None:
    loaders = get_new_context()
    _log("group", id=group_name)
    root_nicknames: Dict[str, str] = {
        root.id: root.state.nickname
        for root in await loaders.group_roots.load(group_name)
    }

    findings: Tuple[Finding, ...]
    findings = await loaders.group_findings.load(group_name)

    # pylint: disable=consider-using-generator
    vulnerabilities: Tuple[Vulnerability, ...] = tuple(
        [
            vuln
            for finding in findings
            for vuln in await loaders.finding_vulnerabilities_nzr.load(
                finding.id
            )
            if vuln.state.status
            in {
                VulnerabilityStateStatus.OPEN,
                VulnerabilityStateStatus.CLOSED,
            }
        ]
    )

    await collect(
        (
            process_toe_inputs(group_name, vulnerabilities),
            process_toe_lines(group_name, vulnerabilities, root_nicknames),
        )
    )


async def main() -> None:
    group_names = await groups_domain.get_active_groups()

    await collect(
        tuple(process_group(group_name) for group_name in group_names),
        workers=5,
    )
