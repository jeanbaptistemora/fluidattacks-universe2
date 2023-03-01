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
    format_forces_report,
)
from forces.report.data import (
    compile_raw_report,
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
            "gathering": "Gathering findings data",
            "processing": "Processing findings data",
            "formatting": "Formatting findings data",
            "uploading": "Uploading Report to ARM",
        }
        footer: str = ": [green]Complete[/]"
        if config.kind == KindEnum.DYNAMIC:
            if config.repository_name:
                await log(
                    "info",
                    (
                        f"Looking for dynamic vulnerabilities associated "
                        f"with the repo: "
                        f"[bright_yellow]{config.repository_name}[/] "
                        f"of group {config.group}."
                    ),
                )
                await log(
                    "info",
                    (
                        "Dynamic vulnerabilities in this group not associated "
                        "with any repos will also be included in the report"
                    ),
                )
        else:
            metadata["git_repo"] = (
                config.repository_name or metadata["git_repo"]
            )
            if config.repository_name:
                await log(
                    "info",
                    (
                        f"Looking for vulnerabilities in the repo: "
                        f"[bright_yellow]{config.repository_name}[/] "
                        f"of group {config.group}"
                    ),
                )
            else:
                await log(
                    "warning",
                    (
                        "No specific repository name has been set. "
                        "Looking for vulnerabilities in [bright_yellow]all[/] "
                        f"repositories registered in {config.group}"
                    ),
                )

            # check if repo is in roots
            if (
                config.repository_name is not None
                and config.kind != KindEnum.ALL
                and not await check_remotes(config)
            ):
                return 1

        await log("info", f"{tasks['gathering']}{footer}")
        report = await compile_raw_report(config)

        if report.summary.total > 0:
            await log("info", f"{tasks['processing']}{footer}")
            forces_report: ForcesReport = format_forces_report(
                config,
                report,
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

        if config.output:
            temp_file.seek(os.SEEK_SET)
            await in_thread(config.output.write, temp_file.read())
        exit_code = await set_forces_exit_code(config, report.findings)
        await upload_report(
            config=config,
            execution_id=str(uuid.uuid4()).replace("-", ""),
            exit_code=str(exit_code),
            report=report,
            log_file=temp_file.name,
            git_metadata=metadata,
        )
        await log("info", f"{tasks['uploading']}{footer}")
        await log("info", f"Success execution: {exit_code == 0}")
    return exit_code
