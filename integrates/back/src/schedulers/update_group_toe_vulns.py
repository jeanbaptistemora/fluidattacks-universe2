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
    Tuple,
)

logging.config.dictConfig(LOGGING)
LOGGER_CONSOLE = logging.getLogger("console")

bugsnag_utils.start_scheduler_session()


def _log(msg: str, **extra: Any) -> None:
    LOGGER_CONSOLE.info(msg, extra={"extra": extra})


def _strip_first_dir(where: str) -> str:
    return where[where.find("/") + 1 :]


async def main() -> None:
    groups = await groups_domain.get_alive_group_names()
    loaders = get_new_context()

    for group in groups:
        _log("group", id=group)

        findings: Tuple[Finding, ...]
        findings = await loaders.group_findings.load(group)

        # pylint: disable=consider-using-generator
        _log("  getting vulnerabilities in all findings")
        vulnerabilities: Tuple[Vulnerability, ...] = tuple(
            [
                vuln
                for finding in findings
                for vuln in await loaders.finding_vulns_nzr_typed.load(
                    finding.id
                )
                if vuln.state.status
                in {
                    VulnerabilityStateStatus.OPEN,
                    VulnerabilityStateStatus.CLOSED,
                }
            ]
        )

        _log("  getting toe inputs")
        group_toe_inputs: Tuple[ToeInput, ...] = tuple(
            edge.node
            for conn in [
                await loaders.group_toe_inputs.load(
                    GroupToeInputsRequest(group_name=group)
                )
            ]
            for edge in conn.edges
        )
        _log("  getting toe lines")
        group_toe_lines: Tuple[ToeLines, ...] = tuple(
            edge.node
            for conn in [
                await loaders.group_toe_lines.load(
                    GroupToeLinesRequest(group_name=group)
                )
            ]
            for edge in conn.edges
        )

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
                _log(
                    "  updating toe_input:",
                    where=toe_input.component,
                    specific=toe_input.entry_point,
                )

                await toe_inputs_domain.update(
                    toe_input,
                    ToeInputAttributesToUpdate(
                        be_present=toe_input.be_present,
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )

        for toe_line in group_toe_lines:
            has_vulnerabilities = any(
                vulnerability.state.status is VulnerabilityStateStatus.OPEN
                and vulnerability.root_id == toe_line.root_id
                and _strip_first_dir(vulnerability.where) == toe_line.filename
                and vulnerability.where == toe_line.filename
                for vulnerability in vulnerabilities
            )

            if toe_line.has_vulnerabilities != has_vulnerabilities:
                _log(
                    "  updating toe_line:",
                    filename=toe_line.filename,
                    has_vulnerabilities=has_vulnerabilities,
                    root_id=toe_line.root_id,
                )

                await toe_lines_domain.update(
                    toe_line,
                    ToeLinesAttributesToUpdate(
                        be_present=toe_line.be_present,
                        has_vulnerabilities=has_vulnerabilities,
                    ),
                )
