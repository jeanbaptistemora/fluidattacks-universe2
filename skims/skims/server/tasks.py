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
from typing import (
    cast,
)
from vulnerabilities import (
    build_metadata,
    search_method,
)


async def get_vulnerabilities(
    execution_id: str, namespace: str
) -> core_model.Vulnerabilities:
    current_results = await get_results(execution_id)
    vulnerabilities: core_model.Vulnerabilities = ()
    for vuln in current_results["runs"][0]["results"]:
        what = vuln["locations"][0]["physicalLocation"]["artifactLocation"][
            "uri"
        ]
        if (
            (properties := vuln.get("properties"))
            and (technique_value := properties.get("technique"))
            and (technique_value == core_model.TechniqueEnum.SCA.value)
            and (message_properties := vuln["message"].get("properties"))
            and (message_properties)
        ):
            what = " ".join(
                (
                    what,
                    (
                        f"({message_properties['dependency_name']} "
                        f"v{message_properties['dependency_version']})"
                    ),
                    f"[{', '.join(message_properties['cve'])}]",
                )
            )
        parsed_vuln = core_model.Vulnerability(
            core_model.FindingEnum[f"F{vuln['ruleId']}"],
            kind=core_model.VulnerabilityKindEnum[
                vuln["properties"]["kind"].upper()
            ],
            state=core_model.VulnerabilityStateEnum.OPEN,
            what=what,
            where=str(
                vuln["locations"][0]["physicalLocation"]["region"]["startLine"]
            ),
            namespace=namespace,
            skims_metadata=build_metadata(
                method=cast(
                    core_model.MethodsEnum,
                    search_method(vuln["properties"]["source_method"]),
                ),
                description=vuln["message"]["text"],
                snippet=vuln["locations"][0]["physicalLocation"]["region"][
                    "snippet"
                ]["text"],
            ),
        )
        vulnerabilities = (*vulnerabilities, parsed_vuln)

    return vulnerabilities


async def report_wrapped(task_id: str) -> None:
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
    asyncio.run(report_wrapped(task_id))
