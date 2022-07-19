from .celery import (
    app,
)
from .resources import (
    get_config,
    get_results,
)
import asyncio
from core.persist import (
    persist,
)
from ctx import (
    CTX,
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


async def _report_wrapped(task_id: str) -> None:
    group = task_id.split("_")[0]
    CTX.config = await get_config(task_id)
    current_results = await get_results(task_id)
    vulnerabilities = [
        core_model.Vulnerability(
            core_model.FindingEnum[result["finding"]],
            kind=core_model.VulnerabilityKindEnum[result["kind"].upper()],
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=result["what"],
            where=result["where"],
            namespace=CTX.config.namespace,
        )
        for result in current_results
    ]
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
    await persist(group=group, stores=stores)


@app.task(serializer="json", name="process-skims-result")
def report(task_id: str) -> None:
    asyncio.run(_report_wrapped(task_id))
