import aioboto3
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.enums import (
    Source,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
)
from db_model.roots.types import (
    GitRoot,
)
from decimal import (
    Decimal,
)
from findings import (
    domain as findings_domain,
)
from findings.types import (
    FindingDraftToAdd,
)
from newutils.findings import (
    get_requirements_file,
    get_vulns_file,
)
import tempfile
from typing import (
    Any,
    cast,
    Dict,
    List,
    Optional,
    Tuple,
)
import yaml  # type: ignore


async def get_config(execution_id: str) -> Dict[str, Any]:
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        with tempfile.NamedTemporaryFile() as temp:
            await s3_client.download_fileobj(
                "skims.data",
                f"configs/{execution_id}.yaml",
                temp,
            )
            temp.seek(0)
            return yaml.safe_load(temp)


async def get_sarif_log(execution_id: str) -> Dict[str, Any]:
    session = aioboto3.Session()
    async with session.client("s3") as s3_client:
        with tempfile.NamedTemporaryFile() as temp:
            await s3_client.download_fileobj(
                "skims.data",
                f"results/{execution_id}.sarif",
                temp,
            )
            temp.seek(0)
            return yaml.safe_load(temp)


def generate_cssv_vector(criteria_vulnerability: Dict[str, Any]) -> str:
    score = criteria_vulnerability["score"]
    base = score["base"]
    temporal = score["temporal"]
    return (
        "CVSS:3.1"
        f"/AV:${base['attack_vector']}/AC:${base['attack_complexity']}"
        f"/PR:${base['privileges_required']}/UI:${base['user_interaction']}"
        f"/S:${base['scope']}/C:${base['confidentiality']}"
        f"/I:${base['integrity']}/A:${base['availability']}"
        f"/E:${temporal['exploit_code_maturity']}"
        f"/RL:${temporal['remediation_level']}"
        f"/RC:${temporal['report_confidence']}"
    )


async def _create_draft(
    group_name: str,
    vulnerability_id: str,
    language: str,
    criteria_vulnerability: Dict[str, Any],
    criteria_requirements: Dict[str, Any],
) -> Finding:
    language = language.lower()
    severity_info = Finding31Severity(
        attack_complexity=Decimal("0.0"),
        attack_vector=Decimal("0.0"),
        availability_impact=Decimal("0.0"),
        confidentiality_impact=Decimal("0.0"),
        exploitability=Decimal("0.0"),
        integrity_impact=Decimal("0.0"),
        privileges_required=Decimal("0.0"),
        remediation_level=Decimal("0.0"),
        report_confidence=Decimal("0.0"),
        severity_scope=Decimal("0.0"),
        user_interaction=Decimal("0.0"),
    )
    draft_info = FindingDraftToAdd(
        attack_vector_description=criteria_vulnerability[language]["impact"],
        description=criteria_vulnerability[language]["description"],
        hacker_email="machine@fluidattacks.com",
        min_time_to_remediate=criteria_vulnerability["remediation_time"],
        recommendation=criteria_vulnerability[language]["recommendation"],
        requirements="\n".join(
            [
                criteria_requirements[item][language]["title"]
                for item in criteria_vulnerability["requirements"]
            ]
        ),
        severity=severity_info,
        threat=criteria_vulnerability[language]["threat"],
        title=(
            f"{vulnerability_id}. "
            f"{criteria_vulnerability[language]['tittle']}"
        ),
    )
    return await findings_domain.add_draft(
        group_name,
        "machine@fluidattacks.com",
        draft_info,
        source=Source.MACHINE,
    )


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    execution_id = ""
    group_name = execution_id.split("_", maxsplit=1)[0]
    execution_config = await get_config(execution_id)
    criteria_vulns = await get_vulns_file()
    criteria_reqs = get_requirements_file()
    try:
        git_root = next(  # noqa  # pylint: disabled=unused-variable
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
            and root.state.nickname == execution_config["namespace"]
        )
    except StopIteration:
        return
    group_findings: Tuple[
        Finding, ...
    ] = await loaders.group_drafts_and_findings.load(group_name)
    results = await get_sarif_log(execution_id)
    rules_id: List[str] = [
        item["id"] for item in results["runs"][0]["tool"]["driver"]["rules"]
    ]
    group_findings = tuple(
        finding
        for finding in group_findings
        if any(rule in finding.title for rule in rules_id)
    )
    rules_finding: Tuple[Tuple[str, Optional[Finding]], ...] = ()
    for vuln_id in rules_id:
        for finding in group_findings:
            if vuln_id in finding.title:
                rules_finding = (*rules_finding, (vuln_id, finding))
                break
        else:
            rules_finding = (*rules_finding, (vuln_id, None))
    for vuln_id, finding in rules_finding:  # type: ignore
        if not finding:
            finding = await _create_draft(
                group_name,
                vuln_id,
                cast(str, execution_config["language"]),
                criteria_vulns[vuln_id],
                criteria_reqs,
            )
