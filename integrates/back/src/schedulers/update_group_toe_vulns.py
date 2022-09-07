# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    collect,
)
from custom_exceptions import (
    ToeInputAlreadyUpdated,
    ToeLinesAlreadyUpdated,
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
from typing import (
    Any,
)

logging.config.dictConfig(LOGGING)
LOGGER = logging.getLogger(__name__)

bugsnag_utils.start_scheduler_session()


def _log(msg: str, **extra: Any) -> None:
    LOGGER.info(msg, extra={"extra": extra})


def _strip_first_dir(where: str) -> tuple[str, str]:
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
    group_name: str, open_vulnerabilities: tuple[Vulnerability, ...]
) -> None:
    loaders = get_new_context()
    group_toe_inputs = await loaders.group_toe_inputs.load_nodes(
        GroupToeInputsRequest(group_name=group_name)
    )
    updations = []
    inputs_types = {VulnerabilityType.INPUTS, VulnerabilityType.PORTS}

    for toe_input in group_toe_inputs:
        has_vulnerabilities: bool = (
            any(
                # ToeInput is not associated to a root_id
                # and vulnerability.root_id == toe_input.root_id
                html.unescape(vulnerability.where).startswith(
                    toe_input.component
                )
                and html.unescape(vulnerability.specific).startswith(
                    toe_input.entry_point
                )
                for vulnerability in open_vulnerabilities
                if vulnerability.type in inputs_types
            )
            if toe_input.be_present
            else False
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
    open_vulnerabilities: tuple[Vulnerability, ...],
    root_nicknames: dict[str, str],
) -> None:
    loaders: Dataloaders = get_new_context()
    group_toe_lines = await loaders.group_toe_lines.load_nodes(
        GroupToeLinesRequest(group_name=group_name)
    )

    updations = []

    for toe_line in group_toe_lines:
        has_vulnerabilities = (
            any(
                vulnerability_where_repo == root_nicknames[toe_line.root_id]
                and vulnerability_where_path.startswith(toe_line.filename)
                for vulnerability in open_vulnerabilities
                if vulnerability.type == VulnerabilityType.LINES
                for vulnerability_where_repo, vulnerability_where_path in [
                    _strip_first_dir(html.unescape(vulnerability.where))
                ]
            )
            if toe_line.be_present
            else False
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


async def get_open_vulnerabilities(
    loaders: Dataloaders,
    finding: Finding,
) -> tuple[Vulnerability, ...]:
    connections: VulnerabilitiesConnection = (
        await loaders.finding_vulnerabilities_nzr_c.load(
            FindingVulnerabilitiesZrRequest(
                finding_id=finding.id,
                paginate=False,
                state_status=VulnerabilityStateStatus.OPEN,
            )
        )
    )
    return tuple(edge.node for edge in connections.edges)


async def process_group(group_name: str) -> None:
    loaders: Dataloaders = get_new_context()
    _log("group", id=group_name)
    root_nicknames: dict[str, str] = {
        root.id: root.state.nickname
        for root in await loaders.group_roots.load(group_name)
    }

    findings: tuple[Finding, ...]
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
                group_name, open_vulnerabilities, root_nicknames
            ),
        )
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    group_names = await orgs_domain.get_all_active_group_names(loaders)

    await collect(
        tuple(process_group(group_name) for group_name in group_names),
        workers=5,
    )
