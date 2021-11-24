from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
)
from boto3.dynamodb.conditions import (
    Key,
)
from dataloaders.utils import (
    format_vulnerability,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from dynamodb import (
    operations_legacy as dynamodb_ops,
)
from typing import (
    List,
    Tuple,
)


async def _get_vulnerabilities_by_root(
    group_findings_loader: DataLoader,
    group_name: str,
    nickname: str,
) -> Tuple[Vulnerability, ...]:
    findings: Tuple[Finding, ...] = await group_findings_loader.load(
        group_name
    )
    finding_ids = {finding.id for finding in findings}
    items = await dynamodb_ops.query(
        "FI_vulnerabilities",
        {
            "IndexName": "repo_index",
            "KeyConditionExpression": Key("repo_nickname").eq(nickname),
        },
    )
    return tuple(
        format_vulnerability(item)
        for item in items
        if item["finding_id"] in finding_ids
    )


class RootVulnsTypedLoader(DataLoader):
    def __init__(self, dataloader: DataLoader) -> None:
        super().__init__()
        self.dataloader = dataloader

    # pylint: disable=method-hidden
    async def batch_load_fn(
        self, root_nicknames: List[Tuple[str, str]]
    ) -> Tuple[Tuple[Vulnerability, ...], ...]:
        return await collect(
            _get_vulnerabilities_by_root(
                group_findings_loader=self.dataloader,
                group_name=group_name,
                nickname=nickname,
            )
            for group_name, nickname in root_nicknames
        )
