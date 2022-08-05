import aioboto3
from dataloaders import (
    Dataloaders,
    get_new_context,
)
from db_model.findings.types import (
    Finding,
)
from db_model.roots.types import (
    GitRoot,
)
import tempfile
from typing import (
    Any,
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


async def main() -> None:
    loaders: Dataloaders = get_new_context()
    execution_id = ""
    group_name = execution_id.split("_", maxsplit=1)[0]
    execution_config = await get_config(execution_id)
    try:
        git_root = next(  # noqa  # pylint: disabled=unused-variable
            root
            for root in await loaders.group_roots.load(group_name)
            if isinstance(root, GitRoot)
            and root.state.nickname == execution_config["namespace"]
        )
    except StopIteration:
        return
    group_findings: Tuple[Finding, ...] = await loaders.group_findings.load(
        group_name
    )
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
    for rule in rules_id:
        for finding in group_findings:
            if rule in finding.title:
                rules_finding = (*rules_finding, (rule, finding))
                break
        else:
            rules_finding = (*rules_finding, (rule, None))
