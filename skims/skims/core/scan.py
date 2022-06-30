from config import (
    load,
)
from contextlib import (
    suppress,
)
from core.persist import (
    persist,
    verify_permissions,
)
import csv
from ctx import (
    CTX,
    MANAGER,
)
from dast.aws.analyze import (
    analyze as analyze_dast_aws,
)
from datetime import (
    datetime,
)
from integrates.domain import (
    do_finish_skims_execution,
    do_start_skims_execution,
)
from integrates.graphql import (
    create_session,
)
from lib_apk.analyze import (
    analyze as analyze_apk,
)
from lib_http.analyze import (
    analyze as analyze_http,
)
from lib_sast.analyze import (
    analyze as analyze_sast,
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
    List,
    Optional,
    Union,
)
from utils.bugs import (
    add_bugsnag_data,
)
from utils.logs import (
    configure as configure_logs,
    log_blocking,
)
from utils.repositories import (
    get_repo_head_hash,
)
from zone import (
    t,
)


async def execute_skims(
    stores: Optional[Dict[core_model.FindingEnum, EphemeralStore]] = None
) -> Dict[core_model.FindingEnum, EphemeralStore]:
    """
    Execute skims according to the provided config.

    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    """
    CTX.value_to_add = value_model.ValueToAdd(MANAGER.dict())

    stores = stores or {
        finding: get_ephemeral_store() for finding in core_model.FindingEnum
    }

    if CTX.config.apk.include:
        analyze_apk(stores=stores)
    if CTX.config.path.include:
        analyze_sast(stores=stores)

    if CTX.config.dast:
        if CTX.config.dast.ssl.include:
            await analyze_ssl(stores=stores)
        if CTX.config.dast.http.include:
            await analyze_http(stores=stores)
        for aws_cred in CTX.config.dast.aws_credentials:
            await analyze_dast_aws(credentials=aws_cred, stores=stores)
    if CTX.config.output:
        notify_findings_as_csv(stores, CTX.config.output)
    else:
        notify_findings_as_snippets(stores)

    log_blocking("info", "Value missing to add:\n%s", CTX.value_to_add)

    return stores


def notify_findings_as_snippets(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    """Print user-friendly messages about the results found."""
    for store in stores.values():
        for result in store.iterate():
            if result.skims_metadata:
                title = t(result.finding.value.title)
                what = result.what_on_integrates
                snippet = result.skims_metadata.snippet
                log_blocking("info", f"{title}: {what}\n\n{snippet}\n")


def notify_findings_as_csv(
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
        for result in store.iterate()
        for snippet in [result.skims_metadata.snippet.replace("\x00", "")]
        if result.skims_metadata
    ]

    with open(output, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in sorted(rows, key=str):
            with suppress(UnicodeEncodeError):
                writer.writerow(row)

    log_blocking("info", "An output file has been written: %s", output)


async def persist_to_integrates(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> Dict[core_model.FindingEnum, core_model.PersistResult]:
    log_blocking("info", f"Results will be sync to group: {CTX.config.group}")
    return await persist(group=CTX.config.group, stores=stores)


async def notify_start(job_id: str) -> None:
    await do_start_skims_execution(
        root=CTX.config.namespace,
        group_name=CTX.config.group,
        job_id=job_id,
        start_date=datetime.utcnow(),
        commit_hash=get_repo_head_hash(CTX.config.working_dir),
    )


async def notify_end(
    job_id: str,
    persisted_results: Dict[core_model.FindingEnum, core_model.PersistResult],
) -> None:
    await do_finish_skims_execution(
        root=CTX.config.namespace,
        group_name=CTX.config.group,
        job_id=job_id,
        end_date=datetime.utcnow(),
        findings_executed=tuple(
            {
                "finding": finding.name,
                "open": get_ephemeral_store().length(),
                "modified": (
                    p_result.diff_result.length()
                    if finding in persisted_results
                    and (p_result := persisted_results[finding])
                    and p_result.diff_result
                    else 0
                ),
            }
            for finding in core_model.FindingEnum
            if finding in CTX.config.checks
        ),
    )


async def main(
    config: Union[str, core_model.SkimsConfig],
    group: Optional[str],
    token: Optional[str],
) -> bool:
    try:
        CTX.config = load(group, config) if isinstance(config, str) else config

        configure_logs()
        add_bugsnag_data(namespace=CTX.config.namespace)

        reset_ephemeral_state()

        log_blocking("info", f"Namespace: {CTX.config.namespace}")
        log_blocking(
            "info",
            f"HEAD is now at: {get_repo_head_hash(CTX.config.working_dir)}",
        )
        log_blocking("info", f"Startup work dir is: {CTX.config.start_dir}")
        log_blocking("info", f"Moving work dir to: {CTX.config.working_dir}")

        os.chdir(CTX.config.working_dir)

        integrates_access = False
        if group and token:
            create_session(token)
            integrates_access = await verify_permissions(group=group)

        persisted_results = {}
        batch_job_id = os.environ.get("AWS_BATCH_JOB_ID")

        if integrates_access and batch_job_id:
            await notify_start(batch_job_id)

        stores = await execute_skims()

        if integrates_access:
            persisted_results = await persist_to_integrates(stores)
        else:
            log_blocking(
                "info",
                (
                    "In case you want to persist results to Integrates "
                    "please make sure you set the --token and --group flag "
                    "in the CLI"
                ),
            )

        success = all(persisted_results.values())

        if integrates_access and batch_job_id:
            await notify_end(batch_job_id, persisted_results)

        return success
    finally:
        if CTX and CTX.config and CTX.config.start_dir:
            os.chdir(CTX.config.start_dir)
            reset_ephemeral_state()


async def execute_set_of_configs(
    configs: List[core_model.SkimsConfig],
    group: Optional[str],
    token: Optional[str],
) -> bool:
    configure_logs()
    reset_ephemeral_state()
    integrates_access = False
    if group and token:
        create_session(token)
        integrates_access = await verify_permissions(group=group)

    batch_job_id = os.environ.get("AWS_BATCH_JOB_ID")

    stores = {
        finding: get_ephemeral_store() for finding in core_model.FindingEnum
    }
    for index, current_config in enumerate(configs):
        CTX.config = current_config
        if integrates_access and batch_job_id:
            await notify_start(batch_job_id)

        add_bugsnag_data(namespace=CTX.config.namespace)

        log_blocking("info", f"Executing config {index+1}: {len(configs)}")
        log_blocking("info", f"Namespace: {CTX.config.namespace}/")
        log_blocking("info", f"Startup work dir is: {CTX.config.start_dir}")
        log_blocking("info", f"Moving work dir to: {CTX.config.working_dir}")

        os.chdir(CTX.config.working_dir)

        stores = await execute_skims(stores)

    persisted_results = {}
    success = True
    if integrates_access:
        persisted_results = await persist_to_integrates(stores)
    else:
        log_blocking(
            "info",
            (
                "In case you want to persist results to Integrates "
                "please make sure you set the --token and --group flag "
                "in the CLI"
            ),
        )

    success = all(persisted_results.values())

    if integrates_access and batch_job_id:
        await notify_end(batch_job_id, persisted_results)

    reset_ephemeral_state()
    return success
