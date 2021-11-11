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
    CONSOLE,
    log,
    LOG_FILE,
)
from forces.utils.model import (
    ForcesConfig,
    KindEnum,
)
import os
from rich.text import (
    Text,
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
    with CONSOLE.status(
        "[bold green]Working on reports...[/]", spinner="aesthetic"
    ):
        tasks = [
            "Resolving repo",
            "Gathering findings data",
            "Processing findings data",
            "Formatting findings data",
            "Uploading Report to ASM",
        ]
        footer: Text = Text.assemble(": ", ("Complete", "green"))
        while tasks:
            if config.kind in {KindEnum.STATIC, KindEnum.ALL}:
                if not config.repository_name:
                    await log(
                        "warning",
                        Text.assemble(
                            "The vulnerabilities of ",
                            ("all", "bright_yellow"),
                            " repositories will be scanned",
                        ),
                    )

                metadata["git_repo"] = (
                    config.repository_name or metadata["git_repo"]
                )
                if config.repository_name:
                    await log(
                        "info",
                        Text.assemble(
                            "Running forces on the repository: ",
                            (config.repository_name, "bright_yellow"),
                        ),
                    )

                # check if repo is in roots
                if (
                    config.repository_name is not None
                    and not await check_remotes(config)
                    and config.kind != KindEnum.ALL
                ):
                    return 1
            await log("info", Text.assemble(tasks.pop(0), footer))
            report = await generate_report(config)
            await log("info", Text.assemble(tasks.pop(0), footer))

            if report["summary"]["total"] > 0:
                filtered_report = filter_report(
                    copy.deepcopy(report), verbose_level=config.verbose_level
                )
                await log("info", f"{tasks.pop(0)}{footer}")
                finding_report, summary_report = format_rich_report(
                    filtered_report, config.verbose_level, config.kind.value
                )
                await log("info", f"{tasks.pop(0)}{footer}")
                CONSOLE.log(finding_report)
                CONSOLE.log(summary_report)
            else:
                tasks.pop(0)
                tasks.pop(0)
                no_vulns_msg: Text = Text(
                    "The current repository has no reported vulnerabilities"
                )
                no_vulns_msg.stylize(style="green")
                await log(
                    "info",
                    no_vulns_msg,
                )

            if output := config.output:
                temp_file.seek(os.SEEK_SET)
                await in_thread(output.write, temp_file.read().decode("utf-8"))
            if config.strict and report["summary"]["open"]["total"] > 0:
                exit_code = 1
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
            )
            await log("info", Text.assemble(tasks.pop(0), footer))
            await log("info", f"Success execution: {exit_code == 0}")
    return exit_code
