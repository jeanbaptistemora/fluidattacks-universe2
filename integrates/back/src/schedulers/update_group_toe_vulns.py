from aioextensions import (
    collect,
)
from custom_exceptions import (
    ToeInputAlreadyUpdated,
    ToeLinesAlreadyUpdated,
    ToePortAlreadyUpdated,
)
from dataloaders import (
    Dataloaders,
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
from db_model.toe_ports.types import (
    GroupToePortsRequest,
    ToePort,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    Vulnerability,
)
from decorators import (
    retry_on_exceptions,
)
from dynamodb.exceptions import (
    UnavailabilityError,
)
import html
from itertools import (
    chain,
)
import logging
import logging.config
from newutils import (
    bugsnag as bugsnag_utils,
)
from organizations import (
    domain as orgs_domain,
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
from toe.ports import (
    domain as toe_ports_domain,
)
from toe.ports.types import (
    ToePortAttributesToUpdate,
)
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

bugsnag_utils.start_scheduler_session()


def _log(msg: str, **extra: Any) -> None:
    LOGGER.info(msg, extra={"extra": extra})


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def update_toe_input(
    current_value: ToeInput, attributes: ToeInputAttributesToUpdate
) -> None:
    await toe_inputs_domain.update(
        current_value=current_value,
        attributes=attributes,
        modified_by="machine@fluidattacks.com",
        is_moving_toe_input=True,
    )


@retry_on_exceptions(
    exceptions=(ToeInputAlreadyUpdated,),
)
async def process_toe_inputs(
    group_name: str, open_vulnerabilities: tuple[Vulnerability, ...]
) -> None:
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    updates = []

    for toe_input in group_toe_inputs:
        has_vulnerabilities: bool = (
            any(
                # ToeInput is not associated to a root_id
                # and vulnerability.root_id == toe_input.root_id
                html.unescape(vulnerability.state.where).startswith(
                    toe_input.component
                )
                and html.unescape(vulnerability.state.specific).startswith(
                    toe_input.entry_point
                )
                for vulnerability in open_vulnerabilities
                if vulnerability.type == VulnerabilityType.INPUTS
            )
            if toe_input.state.be_present
            else False
        )

        if toe_input.state.has_vulnerabilities != has_vulnerabilities:
            updates.append(
                update_toe_input(
                    toe_input,
                    ToeInputAttributesToUpdate(
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
            )

    await collect(tuple(updates))


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
    open_vulnerabilities: tuple[Vulnerability, ...],
) -> None:
    loaders: Dataloaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name)
    )

    updates = []

    for toe_line in group_toe_lines:
        has_vulnerabilities = (
            any(
                vulnerability.state.where.startswith(toe_line.filename)
                for vulnerability in open_vulnerabilities
                if vulnerability.type == VulnerabilityType.LINES
            )
            if toe_line.state.be_present
            else False
        )

        if toe_line.state.has_vulnerabilities != has_vulnerabilities:
            updates.append(
                update_toe_lines(
                    toe_line,
                    ToeLinesAttributesToUpdate(
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
            )

    await collect(tuple(updates))


@retry_on_exceptions(
    exceptions=(UnavailabilityError,),
)
async def update_toe_port(
    current_value: ToePort, attributes: ToePortAttributesToUpdate
) -> None:
    await toe_ports_domain.update(
        current_value,
        attributes,
        "integrates@fluidattacks.com",
        is_moving_toe_port=True,
    )


@retry_on_exceptions(
    exceptions=(ToePortAlreadyUpdated,),
)
async def process_toe_ports(
    group_name: str, open_vulnerabilities: tuple[Vulnerability, ...]
) -> None:
    loaders = get_new_context()
    group_toe_ports = await loaders.group_toe_ports.load_nodes(
        GroupToePortsRequest(group_name=group_name)
    )
    updates = []

    for toe_port in group_toe_ports:
        has_vulnerabilities: bool = (
            any(
                vulnerability.root_id == toe_port.root_id
                and vulnerability.state.specific == toe_port.port
                for vulnerability in open_vulnerabilities
                if vulnerability.type is VulnerabilityType.PORTS
            )
            if toe_port.state.be_present
            else False
        )

        if toe_port.state.has_vulnerabilities != has_vulnerabilities:
            updates.append(
                update_toe_port(
                    toe_port,
                    ToePortAttributesToUpdate(
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
            )

    await collect(tuple(updates))


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    finding: Finding,
) -> tuple[Vulnerability, ...]:
    connections: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_released_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.VULNERABLE,
            )
        )
    )
    return tuple(edge.node for edge in connections.edges)


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    _log("group", id=group_name)
    findings = await loaders.group_findings.load(group_name)
    open_vulnerabilities: tuple[Vulnerability, ...] = tuple(
        chain.from_iterable(
            await collect(
                tuple(
                    get_open_vulnerabilities(loaders, finding)
                    for finding in findings
                )
            )
        )
    )

    await collect(
        (
            process_toe_inputs(group_name, open_vulnerabilities),
            process_toe_lines(
                group_name,
                open_vulnerabilities,
            ),
            process_toe_ports(group_name, open_vulnerabilities),
        )
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)

    await collect(
        tuple(process_group(group_name) for group_name in group_names),
        workers=5,
    )
