from aioextensions import (
    run,
)
from charts import (
    utils,
)
from charts.generators.common.colors import (
    GRAY_JET,
    TREATMENT,
)
from charts.generators.common.utils import (
    get_all_time_forces_executions,
)
from charts.generators.gauge.forces_builds_risk import (
    format_csv_data,
)


async def generate_one(group: str) -> dict:
    executions = await get_all_time_forces_executions(group)
    executions_in_strict_mode = tuple(
        execution
        for execution in executions
        if execution.strictness == "strict"
    )

    executions_in_any_mode_with_accepted_vulns = tuple(
        execution
        for execution in executions
        if execution.vulnerabilities.num_of_accepted_vulnerabilities > 0
        or (
            execution.vulnerabilities.num_of_vulns_in_accepted_exploits
            if execution.vulnerabilities.num_of_vulns_in_accepted_exploits
            else 0
        )
        > 0
    )

    return {
        "color": {
            "pattern": [GRAY_JET, TREATMENT.passive],
        },
        "data": {
            "columns": [
                ["Builds in strict mode", len(executions_in_strict_mode)],
                [
                    "Builds with accepted risk",
                    len(executions_in_any_mode_with_accepted_vulns),
                ],
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
