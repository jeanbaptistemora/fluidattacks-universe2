from .celery import (
    app,
)
from .resources import (
    get_config,
    get_results,
)
import asyncio
from batch.repositories import (
    get_namespace,
)
from core.persist import (
    persist,
)
from ctx import (
    CTX,
)
from integrates.dal import (
    get_group_root_download_url,
    get_group_roots,
)
from integrates.graphql import (
    create_session,
)
from model import (
    core_model,
)
import os
from state.ephemeral import (
    get_ephemeral_store,
)
from typing import (
    Dict,
)
from utils.logs import (
    log_blocking,
)


async def get_vulnerabilities(execution_id: str) -> core_model.Vulnerabilities:
    current_results = await get_results(execution_id)
    vulnerabilities = tuple(
        core_model.Vulnerability(
            core_model.FindingEnum[result["finding"]],
            kind=core_model.VulnerabilityKindEnum[result["kind"].upper()],
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=result["what"].replace(f"{CTX.config.namespace}/", ""),
            where=result["where"],
            namespace=CTX.config.namespace,
        )
        for result in current_results
    )

    return vulnerabilities


async def _report_wrapped(task_id: str) -> None:
    group = task_id.split("_")[0]
    CTX.config = await get_config(task_id)
    vulnerabilities = await get_vulnerabilities(task_id)
    vulns_dict: Dict[core_model.FindingEnum, core_model.Vulnerabilities] = {}
    for vuln in vulnerabilities:
        if vuln.finding not in vulns_dict:
            vulns_dict[vuln.finding] = (vuln,)
        else:
            vulns_dict[vuln.finding] = (
                *vulns_dict[vuln.finding],
                vuln,
            )
    stores = {finding: get_ephemeral_store() for finding in vulns_dict}
    for vuln in vulnerabilities:
        stores[vuln.finding].store(vuln)
    create_session(os.environ["INTEGRATES_API_TOKEN"])
    roots = await get_group_roots(group=group)
    if not vulnerabilities:
        log_blocking("warning", "Execution no has vulnerabilities")
        return
    for root in roots:
        if root.nickname == CTX.config.namespace:
            _, download_url = await get_group_root_download_url(
                group=group, root_id=root.id
            )
            if not download_url:
                log_blocking("warning", "Unable to find presigned url")
                return
            await get_namespace(group, root.nickname, download_url)
            await persist(group=group, stores=stores, roots=roots)
            break


@app.task(serializer="json", name="process-skims-result")
def report(task_id: str) -> None:
    asyncio.run(_report_wrapped(task_id))
