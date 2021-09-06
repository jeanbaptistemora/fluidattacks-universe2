from aioextensions import (
    collect,
)
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from groups import (
    domain as groups_domain,
)
from itertools import (
    chain,
)
from newutils import (
    datetime as datetime_utils,
)
from typing import (
    cast,
    Dict,
    List,
    Set,
    Tuple,
)
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def reset_group_expired_accepted_findings(
    context: Dataloaders, group_name: str, today: str
) -> None:
    finding_vulns_loader = context.finding_vulns
    group_findings_loader = context.group_findings_new

    group_findings: Tuple[Finding] = await group_findings_loader.load(
        group_name
    )
    vulns = list(
        chain.from_iterable(
            await finding_vulns_loader.load_many(
                [finding.id for finding in group_findings]
            )
        )
    )
    findings_to_update: Set[str] = set()

    for vuln in vulns:
        finding_id = cast(str, vuln.get("finding_id"))
        historic_treatment = cast(
            List[Dict[str, str]], vuln.get("historic_treatment", [{}])
        )
        is_accepted_expired = (
            historic_treatment[-1].get("acceptance_date", today) < today
        )
        is_undefined_accepted_expired = (
            (historic_treatment[-1].get("treatment") == "ACCEPTED_UNDEFINED")
            and (
                historic_treatment[-1].get("acceptance_status") == "SUBMITTED"
            )
            and datetime_utils.get_plus_delta(
                datetime_utils.get_from_str(
                    historic_treatment[-1].get(
                        "date", datetime_utils.DEFAULT_STR
                    )
                ),
                days=5,
            )
            <= datetime_utils.get_from_str(today)
        )
        if is_accepted_expired or is_undefined_accepted_expired:
            findings_to_update.add(finding_id)
            updated_values = {"treatment": "NEW"}
            await vulns_domain.add_vulnerability_treatment(
                finding_id=finding_id,
                updated_values=updated_values,
                vuln=vuln,
                user_email=historic_treatment[-1].get("user", ""),
                date=datetime_utils.get_as_str(datetime_utils.get_now()),
            )

    await collect(
        [
            update_unreliable_indicators_by_deps(
                EntityDependency.reset_expired_accepted_findings,
                finding_id=finding_id,
            )
            for finding_id in findings_to_update
        ]
    )


async def reset_expired_accepted_findings() -> None:
    """Update treatment if acceptance date expires"""
    today = datetime_utils.get_now_as_str()
    context: Dataloaders = get_new_context()
    groups = await groups_domain.get_active_groups()
    await collect(
        [
            reset_group_expired_accepted_findings(context, group_name, today)
            for group_name in groups
        ],
        workers=40,
    )


async def main() -> None:
    await reset_expired_accepted_findings()
