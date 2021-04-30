# Third party
from aioextensions import collect

# Local
from batch.dal import delete_action
from batch.types import BatchProcessing
from roots import dal as roots_dal
from vulnerabilities import dal as vulns_dal


async def move_root(*, item: BatchProcessing) -> None:
    old_nickname = item.entity
    new_nickname = item.additional_info
    vulns = await roots_dal.get_root_vulns(nickname=old_nickname)

    await collect(tuple(
        vulns_dal.update(
            vuln['finding_id'],
            vuln['UUID'],
            {'repo_nickname': new_nickname}
        )
        for vuln in vulns
    ))

    await delete_action(
        action_name=item.action_name,
        additional_info=item.additional_info,
        entity=item.entity,
        subject=item.subject,
        time=item.time,
    )
