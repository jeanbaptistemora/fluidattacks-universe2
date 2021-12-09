from config import (
    load,
)
from core.persist import (
    persist,
)
import csv
from datetime import (
    datetime,
)
from integrates.domain import (
    do_add_skims_execution,
)
from lib_apk.analyze import (
    analyze as analyze_apk,
)
from lib_http.analyze import (
    analyze as analyze_http,
)
from lib_path.analyze import (
    analyze as analyze_paths,
)
from lib_root.analyze import (
    analyze as analyze_root,
)
from lib_ssl.analyze import (
    analyze as analyze_ssl,
)
from model import (
    core_model,
    value_model,
)
import os
from state.ephemeral import (
    EphemeralStore,
    get_ephemeral_store,
    reset as reset_ephemeral_state,
)
from typing import (
    Dict,
    Optional,
)
from utils.bugs import (
    add_bugsnag_data,
)
from utils.ctx import (
    CTX,
    MANAGER,
)
from utils.logs import (
    configure as configure_logs,
    log,
)
from zone import (
    t,
)


async def execute_skims(token: Optional[str]) -> bool:
    """Execute skims according to the provided config.

    :param token: Integrates API token
    :type token: str
    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    :return: A boolean indicating success
    :rtype: bool
    """
    success: bool = True
    start_date = datetime.utcnow()
    CTX.value_to_add = value_model.ValueToAdd(MANAGER.dict())

    stores: Dict[core_model.FindingEnum, EphemeralStore] = {
        finding: get_ephemeral_store() for finding in core_model.FindingEnum
    }

    if CTX.config.apk.include:
        await analyze_apk(stores=stores)
    if CTX.config.http.include:
        await analyze_http(stores=stores)
    if CTX.config.path.include:
        if CTX.config.path.lib_path:
            await analyze_paths(stores=stores)
        if CTX.config.path.lib_root:
            await analyze_root(stores=stores)
    if CTX.config.ssl.include:
        await analyze_ssl(stores=stores)

    if CTX.config.output:
        await notify_findings_as_csv(stores, CTX.config.output)
    else:
        await notify_findings_as_snippets(stores)

    await log("info", "Value missing to add:\n%s", CTX.value_to_add)

    if CTX.config.group and token:
        msg = "Results will be synced to group: %s"
        await log("info", msg, CTX.config.group)

        success = await persist(
            group=CTX.config.group,
            stores=stores,
            token=token,
        )
        end_date = datetime.utcnow()
        if batch_job_id := os.environ.get("AWS_BATCH_JOB_ID"):
            executed = tuple(
                {finding.name: {"open": await get_ephemeral_store().length()}}
                for finding in core_model.FindingEnum
            )
            await do_add_skims_execution(
                root=CTX.config.namespace,
                group_name=CTX.config.group,
                job_id=batch_job_id,
                start_date=start_date,
                end_date=end_date,
                findings_executed=executed,
            )
    else:
        success = True
        await log(
            "info",
            (
                "In case you want to persist results to Integrates "
                "please make sure you set the --token and --group flag "
                "in the CLI"
            ),
        )

    return success


async def notify_findings_as_snippets(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found."""
    for store in stores.values():
        async for result in store.iterate():
            if result.skims_metadata:
                title = t(result.finding.value.title)
                what = result.what_on_integrates
                snippet = result.skims_metadata.snippet
                await log("info", f"{title}: {what}\n\n{snippet}\n")


async def notify_findings_as_csv(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    output: str,
) -> None:
    headers = (
        "finding",
        "kind",
        "what",
        "where",
        "cwe",
        "stream",
        "title",
        "description",
        "snippet",
        "method",
    )

    rows = [
        dict(
            cwe=" + ".join(map(str, sorted(result.skims_metadata.cwe))),
            description=result.skims_metadata.description,
            kind=result.kind.value,
            finding=result.finding.name,
            method=result.skims_metadata.source_method,
            snippet=f"\n{snippet}\n",
            stream=result.stream,
            title=t(result.finding.value.title),
            what=result.what_on_integrates,
            where=result.where,
        )
        for store in stores.values()
        async for result in store.iterate()
        for snippet in [result.skims_metadata.snippet.replace("\x00", "")]
        if result.skims_metadata
    ]

    with open(output, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        writer.writerows(sorted(rows, key=str))

    await log("info", "An output file has been written: %s", output)


async def main(
    config: str,
    group: Optional[str],
    token: Optional[str],
) -> bool:
    try:
        CTX.config = load(group, config)
        configure_logs()

        add_bugsnag_data(namespace=CTX.config.namespace)
        await reset_ephemeral_state()
        await log("info", "Namespace: %s", CTX.config.namespace)
        await log("info", "Startup working dir is: %s", CTX.config.start_dir)
        await log("info", "Moving working dir to: %s", CTX.config.working_dir)
        os.chdir(CTX.config.working_dir)
        return await execute_skims(token)
    finally:
        os.chdir(CTX.config.start_dir)
        await reset_ephemeral_state()
