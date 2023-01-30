from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.common.colors import (
    GRAY_JET,
    RISK,
)
from charts.generators.common.utils import (
    get_all_time_forces_executions,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    UnsanitizedInputFound,
)
from db_model.forces.types import (
    ForcesExecution,
)
from newutils.validations import (
    validate_sanitized_csv_input,
)


async def generate_one(*, group: str) -> dict:
    executions = await get_all_time_forces_executions(group)
    executions_in_strict_mode: tuple[ForcesExecution, ...] = tuple(
        execution
        for execution in executions
        if execution.strictness == "strict"
    )

    executions_in_any_mode_with_vulns = tuple(
        execution
        for execution in executions
        if (
            execution.vulnerabilities.num_of_vulns_in_exploits
            if execution.vulnerabilities.num_of_vulns_in_exploits
            else 0
        )
        > 0
        or (
            execution.vulnerabilities.num_of_vulns_in_integrates_exploits
            if execution.vulnerabilities.num_of_vulns_in_integrates_exploits
            else 0
        )
        > 0
        or (
            execution.vulnerabilities.num_of_vulns_in_accepted_exploits
            if execution.vulnerabilities.num_of_vulns_in_accepted_exploits
            else 0
        )
        > 0
        or execution.vulnerabilities.num_of_open_vulnerabilities > 0
        or execution.vulnerabilities.num_of_accepted_vulnerabilities > 0
    )

    successful_executions_in_strict_mode = tuple(
        execution
        for execution in executions_in_strict_mode
        if int(execution.exit_code) == 0
    )

    return {
        "color": {
            "pattern": [GRAY_JET, RISK.more_agressive],
        },
        "data": {
            "columns": [
                [
                    "Successful builds",
                    len(successful_executions_in_strict_mode),
                ],
                ["Vulnerable builds", len(executions_in_any_mode_with_vulns)],
            ],
            "type": "gauge",
        },
        "gauge": {
            "label": {
                "format": None,
                "show": True,
            },
            "max": len(executions),
            "min": 0,
        },
        "gaugeClearFormat": True,
        "legend": {
            "position": "right",
        },
        "paddingRatioTop": 0,
    }


def format_csv_data(*, document: dict) -> utils.CsvData:
    headers: list[str] = ["", ""]
    columns: list[list[str]] = document["data"]["columns"]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(columns[0][0], columns[1][0])
        headers = [columns[0][0], columns[1][0]]

    rows: list[list[str]] = [["", ""]]
    with suppress(UnsanitizedInputFound):
        validate_sanitized_csv_input(str(columns[0][1]), str(columns[1][1]))
        rows = [[str(columns[0][1]), str(columns[1][1])]]

    return utils.CsvData(
        headers=headers,
        rows=rows,
    )


async def generate_all() -> None:
    async for group in utils.iterate_groups():
        document = await generate_one(group=group)
        utils.json_dump(
            document=document,
            entity="group",
            subject=group,
            csv_document=format_csv_data(document=document),
        )


if __name__ == "__main__":
    run(generate_all())
