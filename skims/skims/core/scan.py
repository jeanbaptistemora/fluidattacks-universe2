import aioboto3
from config import (
    dump_to_yaml,
    load,
)
from contextlib import (
    suppress,
)
from core.persist import (
    persist,
    verify_permissions,
)
from core.result import (
    get_sarif,
)
import csv
from ctx import (
    CTX,
    MANAGER,
)
from custom_exceptions import (
    NoOutputFilePathSpecified,
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
import json
from kombu import (
    Connection,
)
from kombu.utils.url import (
    safequote,
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
import tempfile
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
    log_to_remote,
    log_to_remote_blocking,
)
from utils.repositories import (
    get_repo_head_hash,
)
from zone import (
    t,
)


async def _upload_csv_result(
    stores: Dict[core_model.FindingEnum, EphemeralStore]
) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = f"{tmp_dir}/{CTX.config.execution_id}.csv"
        notify_findings_as_csv(stores, file_path)
        with open(file_path, "rb") as reader:
            session = aioboto3.Session()
            async with session.client("s3") as s3_client:
                await s3_client.upload_fileobj(
                    reader,
                    "skims.data",
                    f"results/{CTX.config.execution_id}.csv",
                )


async def upload_sarif_result(
    config: core_model.SkimsConfig,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        file_path = f"{tmp_dir}/{CTX.config.execution_id}.csv"
        notify_findings_as_sarif(
            config=config, stores=stores, output_path=file_path
        )
        with open(file_path, "rb") as reader:
            session = aioboto3.Session()
            async with session.client("s3") as s3_client:
                await s3_client.upload_fileobj(
                    reader,
                    "skims.data",
                    f"results/{CTX.config.execution_id}.sarif",
                )


async def queue_upload_vulns(execution_id: str) -> None:
    access_key = os.environ["AWS_ACCESS_KEY_ID"]
    secret_key = os.environ["AWS_SECRET_ACCESS_KEY"]

    broker_url = f"sqs://{safequote(access_key)}:{safequote(secret_key)}@"
    with Connection(broker_url) as conn:
        queue = conn.SimpleQueue("skims-report-queue")
        message = {
            "id": execution_id,
            "task": "process-skims-result",
            "args": [execution_id],
            "kwargs": {},
            "retries": 0,
            "eta": datetime.now().isoformat(),
        }
        queue.put(message)
        queue.close()


async def execute_skims(
    stores: Optional[Dict[core_model.FindingEnum, EphemeralStore]] = None,
    config: Optional[core_model.SkimsConfig] = None,
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
    config = config or CTX.config
    if config.apk.include:
        analyze_apk(stores=stores)
    if config.path.include:
        analyze_sast(stores=stores)

    if config.dast:
        if config.dast.ssl.include:
            await analyze_ssl(stores=stores)
        if config.dast.http.include:
            await analyze_http(stores=stores)
        for aws_cred in config.dast.aws_credentials:
            if aws_cred:
                await analyze_dast_aws(credentials=aws_cred, stores=stores)
    if config.execution_id:
        await _upload_csv_result(stores)
        await upload_sarif_result(config, stores)
        await queue_upload_vulns(config.execution_id)
    report_results(config=config, stores=stores)

    return stores


def report_results(
    config: core_model.SkimsConfig,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> None:
    if config.output:
        if config.output.format == core_model.OutputFormat.CSV:
            notify_findings_as_csv(
                stores=stores, output=config.output.file_path
            )
        elif config.output.format == core_model.OutputFormat.SARIF:
            notify_findings_as_sarif(config=config, stores=stores)
    else:
        notify_findings_as_snippets(stores)

    log_blocking("info", "Value missing to add:\n%s", CTX.value_to_add)


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
) -> int:
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
        for snippet in [
            result.skims_metadata.snippet.replace("\x00", "")
            if result.skims_metadata
            else ""
        ]
        if result.skims_metadata
    ]

    with open(output, "w", encoding="utf-8") as file:
        writer = csv.DictWriter(file, headers, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for row in sorted(rows, key=str):
            with suppress(UnicodeEncodeError):
                writer.writerow(row)

    log_blocking("info", "An output file has been written: %s", output)
    return len(rows)


def notify_findings_as_sarif(
    config: core_model.SkimsConfig,
    stores: Dict[core_model.FindingEnum, EphemeralStore],
    output_path: Optional[str] = None,
) -> None:
    if output_path is None and config.output is None:
        log_to_remote_blocking(
            msg="No output file path specified for SARIF output",
            severity="warning",
            config=dump_to_yaml(config=config),
        )
        raise NoOutputFilePathSpecified()

    file_path: str
    if output_path is not None:
        file_path = output_path
    elif config.output is not None:
        file_path = config.output.file_path

    result = get_sarif(config, stores)
    with open(file_path, "w", encoding="utf-8") as writer:
        json.dump(result, writer)


async def persist_to_integrates(
    stores: Dict[core_model.FindingEnum, EphemeralStore],
) -> Dict[core_model.FindingEnum, core_model.PersistResult]:
    group = CTX.config.group
    log_blocking("info", f"Results will be sync to group: {group}")
    return await persist(group=group, stores=stores)


async def notify_start(job_id: str, root: Optional[str] = None) -> None:
    await do_start_skims_execution(
        root=root or CTX.config.namespace,
        group_name=CTX.config.group,
        job_id=job_id,
        start_date=datetime.utcnow(),
        commit_hash=CTX.config.commit
        or get_repo_head_hash(CTX.config.working_dir),
    )


async def notify_end(
    job_id: str,
    persisted_results: Dict[core_model.FindingEnum, core_model.PersistResult],
    config: Optional[core_model.SkimsConfig] = None,
) -> None:
    config = config or CTX.config
    await do_finish_skims_execution(
        root=config.namespace,
        group_name=config.group or "",
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
            if finding in config.checks
        ),
    )


async def main(
    config: Union[str, core_model.SkimsConfig],
    group: Optional[str],
    token: Optional[str],
) -> bool:
    try:
        # FP: The function referred to is from another product (reviews)
        CTX.config = (
            load(group, config)  # NOSONAR
            if isinstance(config, str)
            else config
        )

        configure_logs()
        add_bugsnag_data(namespace=CTX.config.namespace)

        reset_ephemeral_state()

        log_blocking("info", f"Namespace: {CTX.config.namespace}")
        commit = CTX.config.commit or get_repo_head_hash(
            CTX.config.working_dir
        )
        log_blocking("info", f"info HEAD is now at: {commit}")
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

    success = True

    for index, current_config in enumerate(configs):
        CTX.config = current_config
        stores = {
            finding: get_ephemeral_store()
            for finding in core_model.FindingEnum
        }

        add_bugsnag_data(namespace=CTX.config.namespace)
        if integrates_access and batch_job_id:
            await notify_start(batch_job_id, root=current_config.namespace)
        else:
            await log_to_remote(
                severity="warning",
                msg="Unable to notify the start of the execution",
                job_id=batch_job_id or "",
                integrates_access=str(integrates_access),
                namespace=current_config.namespace,
            )

        log_blocking("info", f"Executing config {index+1}: {len(configs)}")
        log_blocking("info", f"Namespace: {CTX.config.namespace}/")
        log_blocking("info", f"Startup work dir is: {CTX.config.start_dir}")
        log_blocking("info", f"Moving work dir to: {CTX.config.working_dir}")

        os.chdir(CTX.config.working_dir)

        await execute_skims(stores)
        if batch_job_id and integrates_access:
            await notify_end(
                batch_job_id,
                config=current_config,
                persisted_results={
                    finding: core_model.PersistResult(success=True)
                    for finding in stores.keys()
                },
            )

    reset_ephemeral_state()
    return success
