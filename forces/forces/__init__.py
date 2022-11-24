"""Fluidattacks Forces package."""

from aioextensions import (
    in_thread,
)
from forces.apis.git import (
    check_remotes,
    get_repository_metadata,
)
from forces.apis.integrates import (
    set_api_token,
)
from forces.apis.integrates.api import (
    upload_report,
)
from forces.model import (
    ForcesConfig,
    ForcesReport,
    KindEnum,
)
from forces.report import (
    format_rich_report,
    generate_raw_report,
)
from forces.utils.logs import (
    CONSOLE_INTERFACE,
    log,
    LOG_FILE,
    rich_log,
)
from forces.utils.strict_mode import (
    set_forces_exit_code,
)
import os
import uuid


async def entrypoint(
    token: str,
    config: ForcesConfig,
) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()
    exit_code: int = 0
    set_api_token(token)

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=config.repository_path,
    )
    with CONSOLE_INTERFACE.status(
        "[bold green]Working on reports...[/]", spinner="aesthetic"
    ):
        tasks: dict[str, str] = {
            "resolving": "Resolving repo",
            "gathering": "Gathering findings data",
            "processing": "Processing findings data",
            "formatting": "Formatting findings data",
            "uploading": "Uploading Report to ARM",
        }
        footer: str = ": [green]Complete[/]"
        if config.kind in {KindEnum.STATIC, KindEnum.ALL}:
            metadata["git_repo"] = (
                config.repository_name or metadata["git_repo"]
            )
            if not config.repository_name:
                await log(
                    "warning",
                    (
                        "The vulnerabilities of [bright_yellow]all[/] "
                        "repositories will be scanned"
                    ),
                )

            if config.repository_name:
                await log(
                    "info",
                    (
                        "Running forces on the repository: "
                        f"[bright_yellow]{config.repository_name}[/]"
                    ),
                )

            # check if repo is in roots
            if (
                config.repository_name is not None
                and config.kind != KindEnum.ALL
                and not await check_remotes(config)
            ):
                return 1
        await log("info", f"{tasks['resolving']}{footer}")
        report = await generate_raw_report(config)
        await log("info", f"{tasks['gathering']}{footer}")

        if report.summary.total > 0:
            await log("info", f"{tasks['processing']}{footer}")
            forces_report: ForcesReport = format_rich_report(
                report, config.verbose_level, config.kind
            )
            await log("info", f"{tasks['formatting']}{footer}")
            rich_log(forces_report.findings_report)
            rich_log(forces_report.summary_report)
        else:
            await log(
                "info",
                (
                    "[green]The current repository has no reported "
                    "vulnerabilities[/]"
                ),
            )

        if output := config.output:
            temp_file.seek(os.SEEK_SET)
            await in_thread(output.write, temp_file.read())
        exit_code = await set_forces_exit_code(config, report.findings)
        execution_id = str(uuid.uuid4()).replace("-", "")
        await upload_report(
            group=config.group,
            execution_id=execution_id,
            exit_code=str(exit_code),
            report=report,
            log_file=temp_file.name,
            strictness="strict" if config.strict else "lax",
            git_metadata=metadata,
            kind=config.kind.value,
            grace_period=config.grace_period,
            severity_threshold=config.breaking_severity,
        )
        await log("info", f"{tasks['uploading']}{footer}")
        await log("info", f"Success execution: {exit_code == 0}")
    return exit_code
