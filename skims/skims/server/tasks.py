from . import (
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
from core.scan import (
    notify_end,
)
from ctx import (
    CTX,
)
from integrates.dal import (
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


async def get_vulnerabilities(
    execution_id: str, namespace: str
) -> core_model.Vulnerabilities:
    current_results = await get_results(execution_id)
    vulnerabilities = tuple(
        core_model.Vulnerability(
            core_model.FindingEnum[result["finding"]],
            kind=core_model.VulnerabilityKindEnum[result["kind"].upper()],
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=result["what"],
            where=result["where"],
            namespace=namespace,
        )
        for result in current_results
    )

    return vulnerabilities


async def _report_wrapped(task_id: str) -> None:
    group = task_id.split("_")[0]
    batch_job_id = task_id.split("_")[1]
    load_config = await get_config(task_id)
    CTX.config = load_config

    vulnerabilities = await get_vulnerabilities(task_id, load_config.namespace)
    stores = {finding: get_ephemeral_store() for finding in load_config.checks}
    for vuln in vulnerabilities:
        stores[vuln.finding].store(vuln)
    create_session(os.environ["INTEGRATES_API_TOKEN"])
    roots = await get_group_roots(group=group)

    for root in roots:
        if root.nickname == load_config.namespace:
            if load_config.commit is not None:
                persisted_results = await persist(
                    group=group, stores=stores, roots=roots, config=load_config
                )
                if batch_job_id:
                    await notify_end(
                        batch_job_id, persisted_results, load_config
                    )
                break


@app.task(serializer="json", name="process-skims-result")
def report(task_id: str) -> None:
    asyncio.run(_report_wrapped(task_id))
