import aioboto3
from config import (
    dump_to_yaml,
    load,
)
from contextlib import (
    suppress,
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
import json
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
from utils.bugs import (
    add_bugsnag_data,
)
from utils.logs import (
    configure as configure_logs,
    log_blocking,
    log_to_remote_blocking,
)
from utils.repositories import (
    get_repo_head_hash,
)
from zone import (
    t,
)


async def upload_sarif_result(
    config: core_model.SkimsConfig,
    stores: dict[core_model.FindingEnum, EphemeralStore],
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
                    "machine.data",
                    f"results/{CTX.config.execution_id}.sarif",
                )


async def execute_skims(
    stores: dict[core_model.FindingEnum, EphemeralStore] | None = None,
    config: core_model.SkimsConfig | None = None,
) -> dict[core_model.FindingEnum, EphemeralStore]:
    """
    Execute skims according to the provided config.

    :raises MemoryError: If not enough memory can be allocated by the runtime
    :raises SystemExit: If any critical error occurs
    """
    CTX.value_to_add = value_model.ValueToAdd(MANAGER.dict())  # type: ignore

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
    report_results(config=config, stores=stores)

    return stores


def report_results(
    config: core_model.SkimsConfig,
    stores: dict[core_model.FindingEnum, EphemeralStore],
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
    stores: dict[core_model.FindingEnum, EphemeralStore],
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
    stores: dict[core_model.FindingEnum, EphemeralStore],
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
    stores: dict[core_model.FindingEnum, EphemeralStore],
    output_path: str | None = None,
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


async def main(
    config: str | core_model.SkimsConfig,
    group: str | None,
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

        await execute_skims()

        success = True

        return success
    finally:
        if CTX and CTX.config and CTX.config.start_dir:
            os.chdir(CTX.config.start_dir)
            reset_ephemeral_state()
