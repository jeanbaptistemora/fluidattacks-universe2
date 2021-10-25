"""Fluidattacks Forces package."""

from aioextensions import (
    in_thread,
)
import copy
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
from forces.report import (
    filter_report,
    format_rich_report,
    generate_report,
)
from forces.utils.logs import (
    log,
    LOG_FILE,
)
from forces.utils.model import (
    ForcesConfig,
    KindEnum,
)
import os
from rich import (
    print as rprint,
)
import uuid


async def entrypoint(
    token: str,
    config: ForcesConfig,
) -> int:
    """Entrypoint function"""
    temp_file = LOG_FILE.get()
    exit_code = 0
    set_api_token(token)

    metadata = await in_thread(
        get_repository_metadata,
        repo_path=config.repository_path,
    )
    if config.kind in {KindEnum.STATIC, KindEnum.ALL}:
        if not config.repository_name:
            await log(
                "warning",
                "The vulnerabilities of all repositories will be scanned",
            )

        metadata["git_repo"] = config.repository_name or metadata["git_repo"]
        if config.repository_name:
            await log(
                "info",
                f"Running forces on the repository: {config.repository_name}",
            )

        # check if repo is in roots
        if (
            config.repository_name is not None
            and not await check_remotes(config)
            and config.kind != KindEnum.ALL
        ):
            return 1

    report = await generate_report(config)

    if report["summary"]["total"] > 0:
        filtered_report = filter_report(
            copy.deepcopy(report), verbose_level=config.verbose_level
        )
        finding_report, summary_report = format_rich_report(
            filtered_report, config.verbose_level, config.kind.value
        )
        rprint(finding_report)
        rprint(summary_report)
    else:
        await log(
            "info",
            "[green]The current repository has no reported vulnerabilities[/]",
        )

    if output := config.output:
        temp_file.seek(os.SEEK_SET)
        await in_thread(output.write, temp_file.read().decode("utf-8"))
    if config.strict and report["summary"]["open"]["total"] > 0:
        exit_code = 1
    execution_id = str(uuid.uuid4()).replace("-", "")
    await log("info", "Success execution: %s", exit_code == 0)
    await upload_report(
        group=config.group,
        execution_id=execution_id,
        exit_code=str(exit_code),
        report=report,
        log_file=temp_file.name,
        strictness="strict" if config.strict else "lax",
        git_metadata=metadata,
        kind=config.kind.value,
    )
    return exit_code
